# systemd service

Copy `smartpi.service` to `/etc/systemd/system/`, then:

- Edit `WorkingDirectory` and paths if the repo is not at `/home/pi/rashbarrypi`.
- Ensure `User=` matches the user that has display access (e.g. `pi`).
- Enable and start:
  - `sudo systemctl daemon-reload`
  - `sudo systemctl enable smartpi`
  - `sudo systemctl start smartpi`

Use `journalctl -u smartpi -f` to view logs.
