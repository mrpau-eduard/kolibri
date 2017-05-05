import json
import requests
import os
import sys


USERNAME = os.environ["GITHUB_USERNAME"]
PASSWORD = os.environ['GITHUB_PASSWORD']
TOKEN = os.environ["GITHUB_TOKEN"]
ISSUE_ID = os.environ["GITHUB_ISSUE_ID"]
REPO_OWNER = "mrpau-eduard"
REPO_NAME = "kolibri"

# Buildkite
BUILDKITE_USERNAME = os.environ['BUILDKITE_USERNAME']
BUILDKITE_PASSWORD = os.environ['BUILDKITE_PASSWORD']
BUILDKITE_COMMIT = os.environ['BUILDKITE_COMMIT']

def create_github_comment(windows_installer):
    """Create an comment on github.com using the given parameters."""
    url = 'https://api.github.com/repos/%s/%s/issues/%s/comments' % (REPO_OWNER, REPO_NAME, ISSUE_ID)
    session = requests.Session()
    comment_message = {'body':
                        "## Build Artifact from our servers\r\n"
                        "**Built Kolibri Installers**\r\n"
                        "Windows Installer: %s\r\n"
                        "Mac Installer: Mac.dmg\r\n"
                        "Debian Installer: Debian.deb\r\n\r\n"
                        "**Built Python packages**\r\n"
                        "Pex: kolibri.pex\r\n"
                        "WHL file: kolibri.whl\r\n"
                        "ZIP file: kolibri.zip\r\n"
                        "TAR file: kolibri.tar.gz\r\n"
                        % windows_installer}
    
    r = session.post(url, json.dumps(comment_message), auth=(REPO_OWNER, PASSWORD))
    if r.status_code == 201:
        print 'Successfully created Github comment.'
    else:
        print 'Could not create Github comment. Now exiting!'
        sys.exit(1)
        
def build_kolibri_installer():
    """Trigger the build for the kolibri installer"""
    buildkite_url = 'https://api.buildkite.com/v2/organizations/learningequality/pipelines/mrpau-rocket-build/builds'
    session = requests.Session()
    json_data = {
                "commit": BUILDKITE_COMMIT,
                "branch": "develop",
                "message": "Build installer artifact."
                }
    r = session.post(buildkite_url, json.dumps(json_data), auth=(BUILDKITE_USERNAME, BUILDKITE_PASSWORD))
    if r.status_code == 201:
        print 'Successfully created a installer Artifact.'
    else:
        print 'Could not create installer Artifact. Now exiting!'
        sys.exit(1)

create_github_comment('KolibriSetup-03.1b2.dev6.exe')
build_kolibri_installer()

