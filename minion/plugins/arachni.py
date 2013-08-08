# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.



import json
import time
from minion.plugins.base import ExternalProcessPlugin



def _minion_severity(severity):
    if severity == 'Informational':
        return 'Info'
    return severity

def parse_arachni_output(output_file):
    with open(output_file) as f:
        data = json.load(f)
    
    issues = []
    for issue in data["issues"]:
        issues.append({"Summary": issue["name"], 
            "Severity": _minion_severity(issue["severity"]),
            "URL": issue["url"]})
            # TODO: Add more info from Arachni output file
            # Sample file: 
            # https://github.com/Arachni/arachni/blob/master/spec/support/fixtures/auditstore.afr?raw=true
            # Convert with:
            # arachni --repload=auditstore.afr --report=json:outfile=arachni_sample_file.json
    
    return issues


class ArachniPlugin(ExternalProcessPlugin):

    PLUGIN_NAME = "Arachni"
    PLUGIN_VERSION = "0.1"
    ARACHNI_NAME = "arachni"


    def do_start(self):
        arachni_path = self.locate_program(self.ARACHNI_NAME)
        self.arachni_output_file = "arachni." + time.strftime("%Y-%m-%d_%H-%M-%S") + ".json"
        if arachni_path is None:
            raise Exception("Cannot find arachni in path")
        self.arachni_stdout = ""
        self.arachni_stderr = ""
        target = self.configuration['target']
        args = []
        # TODO: Add good default option / load options from user input
        # https://github.com/Arachni/arachni/wiki/Command-line-user-interface
        args += ["--report=json:outfile=" + self.arachni_output_file]
        args += [target]
        self.spawn(arachni_path, args)

    def do_process_stdout(self, data):
        self.arachni_stdout += data

    def do_process_stderr(self, data):
        self.arachni_stderr += data

    def do_process_ended(self, status):
        if self.stopping and status == 9:
            self.report_finish("STOPPED")
        elif status == 0:
            with open("arachni.stdout.txt", "w") as f:
                f.write(self.arachni_stdout)
            with open("arachni.stderr.txt", "w") as f:
                f.write(self.arachni_stderr)
            self.report_artifacts("Arachni Output", ["arachni.stdout.txt", "arachni.stderr.txt", self.arachni_output_file])
            issues = parse_arachni_output(self.arachni_output_file)
            self.report_issues(issues)
            self.report_finish()
        else:
            self.report_finish("FAILED")

