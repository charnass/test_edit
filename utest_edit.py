import unittest
import requests
import json
import random
import string

token = '1181363a76f49eb2349fb13eda23723ab734680d'

headerstoken = {
        'Content-Type':'application/json',
        'Authorization': 'token %s' % token,
        }

class TestEditIssue(unittest.TestCase):
    def setUp(self):
        self.urltest = "https://api.github.com/repos/charnass/test_edit/issues/2"

    def run(self, result=None):
        if result.failures or result.errors:
            print ("aborted")
        else:
            super(TestEditIssue, self).run(result)

    def test_edit_issue_success(self):
        edit_parameter_set = dict()
        edit_parameter_set['title'] = 'Found a bug'
        edit_parameter_set["body"]  =  "I'm having a problem with this."
        edit_parameter_set["assignees"] = ["charnass"]
        edit_parameter_set["milestone"] = 2
        edit_parameter_set["state"] = "open"
        edit_parameter_set["labels"] = ["bug"]
        response = requests.patch(self.urltest, data=json.dumps(edit_parameter_set), headers=headerstoken)
        self.assertEqual(response.status_code, 200)

    def test_edit_issue_null(self):
        edit_parameter_set_null = dict()
        response = requests.patch(self.urltest, data=json.dumps(edit_parameter_set_null), headers=headerstoken)
        self.assertEqual(response.status_code, 200)

    def test_edit_issue_incomplete (self):
        edit_parameter_set_incomplete = dict()
        edit_parameter_set_incomplete["title"] = "incomplete set title & body"
        edit_parameter_set_incomplete["body"] = "I'm having a incomplete set."

        response = requests.patch(self.urltest, data=json.dumps(edit_parameter_set_incomplete), headers=headerstoken)
        self.assertEqual(response.status_code, 200)

        edit_parameter_set_response = json.loads(requests.get(self.urltest).text)
        self.assertEqual(edit_parameter_set_response["title"], edit_parameter_set_incomplete["title"])
        self.assertEqual(edit_parameter_set_response["body"], edit_parameter_set_incomplete["body"])

    def test_edit_issue_state (self):
        edit_parameter_set_state = dict()
        edit_parameter_set_state['title'] = 'Found a bug'
        edit_parameter_set_state["body"]  =  "I'm having a problem with this."
        edit_parameter_set_state["assignees"] = ["charnass"]
        edit_parameter_set_state["milestone"] = 2
        edit_parameter_set_state["labels"] = ["bug"]
        edit_parameter_set_state["state"] = [random.SystemRandom().choice(string.ascii_letters) for _ in range(5)]

        edit_parameter_response = json.loads(requests.get(self.urltest).text)
        list_stat = ("open", "closed")
        self.assertIn(edit_parameter_response["state"], list_stat, "state не имеет значение open or closed")

        response = requests.patch(
            self.urltest,
            data=json.dumps(edit_parameter_set_state),
            headers=headerstoken).status_code
        self.assertEqual(response, 422)

    def test_edit_issue_assignees_false(self):
        edit_parameter_set_state_false = dict()
        edit_parameter_set_state_false['title'] = 'Found a stat'
        edit_parameter_set_state_false["body"]  = "I'm make false state."
        edit_parameter_set_state_false["assignees"] = ["ololol"]
        edit_parameter_set_state_false["milestone"] = 2
        edit_parameter_set_state_false["state"] = "close"
        edit_parameter_set_state_false["labels"] = ["bug"]

        response = requests.patch(self.urltest, data=json.dumps(edit_parameter_set_state_false), headers=headerstoken)
        self.assertTrue(response.status_code, 422)

    def test_edit_issue_labels(self):
        edit_parameter_set_labels = dict()
        edit_parameter_set_labels['title'] = 'Found a stat'
        edit_parameter_set_labels["body"]  = "I'm make false state."
        edit_parameter_set_labels["assignees"] = ["charnass"]
        edit_parameter_set_labels["milestone"] = 2
        edit_parameter_set_labels["state"] = "close"

        response_labels = json.loads(requests.get("https://api.github.com/repos/charnass/test_edit/labels").text)

        labels_load = set()
        for label in response_labels:
            labels_load.add(label["name"])

        edit_parameter_set_labels["labels"] = [random.SystemRandom().choice(list(labels_load))]
        requests.patch(self.urltest, data=json.dumps(edit_parameter_set_labels), headers=headerstoken)
        edit_parameter_label = json.loads(requests.get(self.urltest).text)["labels"]

        self.assertEqual(edit_parameter_label[0]["name"], edit_parameter_set_labels["labels"][0])
        self.assertIn(edit_parameter_label[0]["name"], labels_load)

    def test_edit_issue_milestone(self):
        edit_parameter_set_state_false = dict()
        edit_parameter_set_state_false['title'] = 'Found a stat'
        edit_parameter_set_state_false["body"]  = "I'm make false state."
        edit_parameter_set_state_false["assignees"] = ["charnass"]
        edit_parameter_set_state_false["state"] = "close"
        edit_parameter_set_state_false["labels"] = ["bug"]

        response_milestone = json.loads(requests.get("https://api.github.com/repos/charnass/test_edit/milestones").text)
        labels_milestone = set()
        for label in response_milestone:
            labels_milestone.add(label["number"])

        edit_parameter_set_state_false["milestone"] = max(labels_milestone) + 1
        self.assertEqual(
            requests.patch(
                self.urltest, data=json.dumps(edit_parameter_set_state_false),
                headers=headerstoken).status_code,
                422
        )

if __name__ == '__main__':
    response = requests.get("https://api.github.com/users/charnass").headers
    if (int(response["X-RateLimit-Remaining"]) > 10):
        unittest.main()
    else:
        print ("aborted: 403 API rate limit exceeded, X-RateLimit-Limit < 10")