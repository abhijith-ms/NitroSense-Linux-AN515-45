# GUI integration changes

Based on the NitroSense revision in upstream.lock.json; app and service source
are tracked locally. Upstream license retained in UPSTREAM-LICENSE.

Build with Node >=22.12: npm ci --ignore-scripts in app, then explicitly run
node node_modules/electron/install.js to download the checksummed runtime.
Use npm run build, npm run typecheck and npm test in app. Never substitute
npm run test:e2e for these tests: those upstream scripts write live hardware.

Run python -m unittest discover -s tests for backend access-policy tests.
The daemon validates inputs independently of frontend checks and disables
module reconfiguration commands. UID/GID in packaging/nitrosense-access.conf
are specific to this laptop and must be generated per installation for others.

scripts/install-service.sh installs root-owned service sources and starts the
service but does not enable boot startup or load a kernel driver. It requires
administrator access. The desktop launcher is a local-development launcher
and depends on this project staying at its current path.

For future distribution: finish packaging the GUI/service (driver DKMS package is now installed), resolve driver license
metadata, test DKMS update/rollback, fix build dependency advisories, validate
suspend/recovery, and expand per-model hardware validation. Do not claim all
Windows NitroSense features on every Acer model. Unsupported firmware controls
must remain visibly unavailable.
