<?php
include_once APP . 'Model/WorkflowModules/WorkflowBaseModule.php';

class Module_validate extends Module_webhook
{
    public $blocking = false;
    public $disabled = true;
    public $id = 'excercise-validate';
    public $name = 'Excercise :: Validate';
    public $description = 'Validate the output';
    public $icon = 'tasks';
    public $inputs = 1;
    public $outputs = 0;
    public $expect_misp_core_format = true;
    public $params = [];

    private $User;

    private $URL = 'http://host.docker.internal:4001/webhook';

    public function __construct()
    {
        parent::__construct();
        $this->User = ClassRegistry::init('User');
        $this->params = [
            [
                'id' => 'message',
                'label' => 'Message',
                'type' => 'input',
                'default' => '',
                'placeholder' => __('Type a message'),
                'jinja_supported' => true,
            ],
        ];
    }

    public function exec(array $node, WorkflowRoamingData $roamingData, array &$errors = []): bool
    {
        parent::exec($node, $roamingData, $errors);
        $this->validate($roamingData, $node);
        return true;
    }

    public function validate(WorkflowRoamingData $rdata, array $node)
    {
        $url = $this->URL;

        // Reset any active filters
        $tmprData = $rdata->getData();
        if (!empty($tmprData['enabledFilters'])) {
            $newRData = $tmprData['_unfilteredData'];
            $newRData['enabledFilters'] = [];
            $rdata->setData($newRData);
        }

        $event = $rdata->getData();
        $params = $this->getParamsWithValues($node, $rdata->getData());
        $message = $params['message']['value'];

        if (!empty($rdata->__secret)) {
            $event['_secret'] = $rdata->__secret;
        }
        $payload = [
            'email' => $this->getEmailFromEventInfo($event),
            'target_tool' => 'MISP Workflow :: Validation',
            'dashboard_message' => $message,
            'data' => $event,
        ];
        $initiatorUser = $rdata->getInitiatorUser();
        $header = 'Something went wrong while validating the Event';

        try {
            $response = $this->doRequest($url, 'json', $payload, [], 'post', ['self_signed' => true]);
            if ($response->isOk()) {
                return true;
            }
            if ($response->code === 403 || $response->code === 401) {
                $errors[] = __('Authentication failed.');
                return false;
            }
            $errors[] = __('Something went wrong with the request or the remote side is having issues. Body returned: %s', $response->body);
            $this->User->createNotificationToast($initiatorUser, $header, implode(', ', $errors), 'danger');
            return false;
        } catch (SocketException $e) {
            $errors[] = __('Something went wrong while sending the request. Error returned: %s', $e->getMessage());
            $this->User->createNotificationToast($initiatorUser, $header, implode(', ', $errors), 'danger');
            return false;
        } catch (Exception $e) {
            $errors[] = __('Something went wrong. Error returned: %s', $e->getMessage());
            $this->User->createNotificationToast($initiatorUser, $header, implode(', ', $errors), 'danger');
            return false;
        }
        $errors[] = __('Something went wrong with the request or the remote side is having issues.');
        $this->User->createNotificationToast($initiatorUser, $header, implode(', ', $errors), 'danger');
        return false;
    }

    private function getEmailFromEventInfo($event)
    {
        $info = $event['Event']['info'];
        $email = explode('Workflow Exercise - ', $info)[1];
        return $email;
    }
}
