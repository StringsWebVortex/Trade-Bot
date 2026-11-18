# Local Kubernetes dev loop: kind cluster "tradebot". Run `tilt up` from the repo root.
# Python source edits are synced into the running containers and Tilt restarts the
# process itself; nothing needs a manual rebuild or restart.
allow_k8s_contexts('kind-tradebot')

load('ext://restart_process', 'docker_build_with_restart')

SRC_ONLY = ['Dockerfile', 'requirements.txt', 'src', 'common', 'config', 'scripts']

def tradebot_image(name, entrypoint):
    docker_build_with_restart(
        name,
        '.',
        dockerfile='Dockerfile',
        target='runtime',
        only=SRC_ONLY,
        entrypoint=entrypoint,
        live_update=[
            sync('src', '/app/src'),
            sync('common', '/app/common'),
            sync('config', '/app/config'),
            sync('scripts', '/app/scripts'),
        ],
    )

tradebot_image('tradebot-api', ['python', '-m', 'src.api'])
tradebot_image('tradebot-worker', ['python', '-m', 'src.workers'])

# Dev secrets are created once and kept across runs, so the operator secret stays valid.
secret_create = (
    'kubectl -n tradebot create secret generic tradebot-secrets'
    + ' --from-literal=API_SECRET_KEY=$(openssl rand -hex 32)'
    + ' --from-literal=OPERATOR_SECRET=$(openssl rand -hex 32)'
)
secret_cmd = (
    'kubectl apply -f deploy/k8s/tradebot.yaml >/dev/null && '
    + 'kubectl -n tradebot get secret tradebot-secrets >/dev/null 2>&1 || '
    + secret_create
)
local_resource('dev-secrets', cmd=secret_cmd, labels=['setup'])

k8s_yaml('deploy/k8s/tradebot.yaml')

k8s_resource('tradebot-api', port_forwards='8000:8000', labels=['app'], resource_deps=['dev-secrets'])
k8s_resource('tradebot-worker', labels=['app'], resource_deps=['dev-secrets'])

# Tests run on this machine with the local Python, and only when triggered from the Tilt UI.
local_resource(
    'tests',
    cmd='python -m pytest -q',
    trigger_mode=TRIGGER_MODE_MANUAL,
    auto_init=False,
    labels=['test'],
)
