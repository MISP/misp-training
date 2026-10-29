<?php
/**
 * Training-only dashboard widget: the authenticated user's own sign-in times.
 * Install as app/Lib/Dashboard/Custom/TrainingLoginSummaryWidget.php.
 */
class TrainingLoginSummaryWidget
{
    public $title = 'Training: my sign-in history';
    public $description = 'Bounded personal sign-in history; no IP addresses or other users\' records.';
    public $category = 'status';
    public $render = 'SimpleList';
    public $width = 4;
    public $height = 4;
    public $params = [];
    public $schema = [
        'lookback' => [
            'type' => 'time_window',
            'default' => 'P7D',
            'help' => 'Look back at most 366 days, or use All. Only your own sign-ins are queried.',
        ],
        'limit' => [
            'type' => 'int',
            'default' => 5,
            'help' => 'Maximum number of sign-ins, from 1 to 10.',
        ],
        'show_org' => [
            'type' => 'bool',
            'default' => false,
            'help' => 'Also display your authenticated organisation name.',
        ],
        'caption' => [
            'type' => 'string',
            'default' => 'Recent sign-ins',
            'help' => 'Plain-text row title, at most 120 UTF-8 bytes.',
        ],
    ];
    public $placeholder = '{"lookback":"P7D","limit":5,"show_org":false,"caption":"Recent sign-ins"}';
    public $autoRefreshDelay = 60;
    public $cache_duration = 30;
    public $cache_scope = 'user';

    public function checkPermissions($user)
    {
        return is_array($user)
            && isset($user['id'])
            && (is_int($user['id']) || is_string($user['id']))
            && filter_var($user['id'], FILTER_VALIDATE_INT, ['options' => ['min_range' => 1]]) !== false;
    }

    public function handler($user, $options = [])
    {
        if (!$this->checkPermissions($user)) {
            throw new ForbiddenException('An authenticated user is required.');
        }
        if (!is_array($options)) {
            throw new BadRequestException('Widget configuration must be an object.');
        }
        // alias and refresh_delay belong to the framework, not this data query.
        $allowed = ['lookback', 'limit', 'show_org', 'caption', 'alias', 'refresh_delay'];
        if (array_diff(array_keys($options), $allowed)) {
            throw new BadRequestException('Unknown widget option.');
        }
        $seconds = $this->windowSeconds(array_key_exists('lookback', $options) ? $options['lookback'] : '7d');
        $limit = array_key_exists('limit', $options) ? $options['limit'] : 5;
        $showOrg = array_key_exists('show_org', $options) ? $options['show_org'] : false;
        $caption = array_key_exists('caption', $options) ? $options['caption'] : 'Recent sign-ins';
        if (!is_int($limit) || $limit < 1 || $limit > 10) {
            throw new BadRequestException('limit must be an integer from 1 to 10.');
        }
        if (!is_bool($showOrg)) {
            throw new BadRequestException('show_org must be a boolean.');
        }
        if (!is_string($caption) || trim($caption) === '' || strlen($caption) > 120
            || preg_match('//u', $caption) !== 1 || preg_match('/[\x00-\x1F\x7F]/', $caption)) {
            throw new BadRequestException('caption must be nonempty UTF-8 text of at most 120 bytes, without control characters.');
        }

        // Never take the identity from configuration. This is an explicit data scope.
        $conditions = ['Log.user_id' => (int)$user['id'], 'Log.action' => 'login'];
        if ($seconds !== -1) {
            // Log::beforeSave uses date() too: keep the application's PHP timezone.
            $conditions['Log.created >='] = date('Y-m-d H:i:s', time() - $seconds);
        }
        $entries = ClassRegistry::init('Log')->find('all', [
            'recursive' => -1,
            'conditions' => $conditions,
            'fields' => ['Log.created'],
            'order' => ['Log.created' => 'DESC', 'Log.id' => 'DESC'],
            'limit' => $limit,
        ]);
        $times = [];
        foreach ($entries as $entry) {
            $times[] = (string)$entry['Log']['created'];
        }
        $rows = [
            ['title' => 'Signed-in user ID', 'value' => (string)$user['id']],
            ['title' => $caption, 'value' => $times ?: 'No matching sign-ins.'],
        ];
        if ($showOrg) {
            $rows[] = ['title' => 'Organisation', 'value' => (string)($user['Organisation']['name'] ?? 'Unavailable')];
        }
        // SimpleList escapes title/value. Do not put these strings into html/html_title.
        return $rows;
    }

    private function windowSeconds($value)
    {
        if ($value === -1 || $value === '-1') {
            return -1;
        }
        if (is_string($value) && preg_match('/^([1-9][0-9]{0,2})d$/D', $value, $match)) {
            $value = (int)$match[1] * 86400;
        } elseif (is_string($value) && strlen($value) <= 8 && ctype_digit($value)) {
            $value = (int)$value;
        }
        if (!is_int($value) || $value < 1 || $value > 366 * 86400) {
            throw new BadRequestException('lookback must be 1-366 days, positive seconds up to 366 days, or -1 for all time.');
        }
        return $value;
    }
}
