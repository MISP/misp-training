<?php
/**
 * Offline contract checks, not an HTTP/database integration test.
 * Usage: php verify_widget.php /path/to/MISP
 * Uses real CakePHP helpers, MISP's adapter/cache-key code and SimpleList.
 * Only Log::find is replaced with an in-memory query recorder.
 */
error_reporting(E_ALL & ~E_DEPRECATED);
$root = isset($argv[1]) ? rtrim($argv[1], '/') : '';
$cake = $root . '/app/Lib/cakephp/lib/Cake/';
if (!is_file($cake . 'basics.php')) {
    fwrite(STDERR, "Supply a MISP checkout with its CakePHP submodule installed.\n");
    exit(2);
}
require $cake . 'basics.php';
require $cake . 'Core/App.php';
require $cake . 'Core/Configure.php';
require $cake . 'Utility/Hash.php';
require $cake . 'Utility/Inflector.php';
require $cake . 'Utility/ClassRegistry.php';
require $cake . 'Error/exceptions.php';
Configure::write('App.encoding', 'UTF-8');
Configure::write('MISP.baseurl', 'https://misp.example.test');
foreach (['WidgetSchema', 'CanonicalTypeAdapter', 'WidgetCache', 'DashboardURLValidator'] as $helper) {
    require $root . '/app/Lib/Dashboard/Tools/' . $helper . '.php';
}
require __DIR__ . '/TrainingLoginSummaryWidget.php';

class Log
{
    public $query;
    public $entries = [];
    public $fail = false;
    public function find($type, $query)
    {
        if ($type !== 'all') {
            throw new RuntimeException('Unexpected query type');
        }
        $this->query = $query;
        if ($this->fail) {
            throw new RuntimeException('Simulated database failure');
        }
        return $this->entries;
    }
}
$log = new Log();
ClassRegistry::addObject('Log', $log);
$widget = new TrainingLoginSummaryWidget();
$user = ['id' => '21', 'org_id' => '7', 'Organisation' => ['name' => 'Training & research']];
$other = array_replace($user, ['id' => '22']);
$checks = 0;
function check($ok, $label)
{
    global $checks;
    if (!$ok) {
        throw new RuntimeException('FAIL: ' . $label);
    }
    ++$checks;
}
function rejected($call, $exception)
{
    try {
        $call();
    } catch (Throwable $e) {
        check($e instanceof $exception, 'expected ' . $exception . ', got ' . get_class($e));
        return;
    }
    throw new RuntimeException('FAIL: expected ' . $exception);
}
function runWidget($options = [])
{
    global $widget, $user;
    return $widget->handler($user, CanonicalTypeAdapter::translate($widget, $options));
}

check(WidgetSchema::validate($widget->schema) === null, 'valid schema');
check($widget->checkPermissions($user), 'authenticated identity accepted');
foreach ([[], ['id' => 0], ['id' => true], ['id' => 'bad'], ['id' => []]] as $invalid) {
    check(!$widget->checkPermissions($invalid), 'invalid identity denied');
}
rejected(function () use ($widget) { $widget->handler([]); }, 'ForbiddenException');
rejected(function () use ($widget, $user) { $widget->handler($user, 'bad'); }, 'BadRequestException');

$rows = runWidget();
check($rows[0]['value'] === '21', 'identity comes from authenticated user');
check($rows[1]['value'] === 'No matching sign-ins.', 'honest empty state');
check($log->query['conditions']['Log.user_id'] === 21, 'query limited to own user');
check($log->query['conditions']['Log.action'] === 'login', 'only login records');
check($log->query['fields'] === ['Log.created'], 'no IP/email selected');
check($log->query['limit'] === 5 && $log->query['recursive'] === -1, 'bounded query');
check($log->query['order'] === ['Log.created' => 'DESC', 'Log.id' => 'DESC'], 'stable newest-first ordering');
foreach (['P7D' => 604800, 'P2W' => 1209600, 'PT6H' => 21600, '7d' => 604800, '3600' => 3600] as $input => $seconds) {
    $before = time();
    runWidget(['lookback' => $input]);
    $cutoff = strtotime($log->query['conditions']['Log.created >=']);
    check(abs(($before - $seconds) - $cutoff) <= 2, 'adapted time window ' . $input);
}
foreach ([-1, '-1'] as $all) {
    runWidget(['lookback' => $all, 'limit' => 10]);
    check(!isset($log->query['conditions']['Log.created >=']) && $log->query['limit'] === 10, 'all time stays bounded');
}
foreach ([null, '', 0, true, 'P367D', [], 'nonsense', 31622401] as $bad) {
    rejected(function () use ($bad) { runWidget(['lookback' => $bad]); }, 'BadRequestException');
}
foreach ([null, '5', 0, 11, true, 5.0] as $bad) {
    rejected(function () use ($bad) { runWidget(['limit' => $bad]); }, 'BadRequestException');
}
foreach ([null, 'false', 0, 1, []] as $bad) {
    rejected(function () use ($bad) { runWidget(['show_org' => $bad]); }, 'BadRequestException');
}
foreach ([null, '', ' ', str_repeat('x', 121), "bad\ntext", "\xFF"] as $bad) {
    rejected(function () use ($bad) { runWidget(['caption' => $bad]); }, 'BadRequestException');
}
rejected(function () { runWidget(['user_id' => 22]); }, 'BadRequestException');
$log->entries = [['Log' => ['created' => '2026-10-29 10:00:00']]];
$config = ['caption' => '<script>alert(1)</script>', 'show_org' => true];
$original = $config;
$data = runWidget($config);
check($config === $original, 'caller configuration unchanged');
check($data[1]['value'] === ['2026-10-29 10:00:00'], 'renderer receives an array of plain text');
check($data[2]['value'] === 'Training & research', 'organisation comes from auth context');
ob_start();
include $root . '/app/View/Elements/dashboard/Widgets/SimpleList.ctp';
$html = ob_get_clean();
check(strpos($html, '<script>') === false && strpos($html, '&lt;script&gt;') !== false, 'actual renderer escapes caption');
check(strpos($html, 'Training &amp; research') !== false && strpos($html, '&amp;amp;') === false, 'actual renderer escapes once');
check(WidgetCache::isCacheable($widget), 'current cache opt-in recognised');
$key = WidgetCache::key($widget, $config, $user);
check($key !== WidgetCache::key($widget, $config, $other), 'same-org users have distinct real cache keys');
check($key === WidgetCache::key($widget, $config + ['alias' => 'A', 'refresh_delay' => 120], $user), 'framework fields are cache-neutral');
check($data === runWidget($config + ['alias' => 'A', 'refresh_delay' => 120]), 'framework fields are data-neutral too');
$log->fail = true;
rejected(function () { runWidget(); }, 'RuntimeException');
echo "PASS: $checks contract checks (real adapter/cache keys/renderer; recorded Log boundary).\n";
