# CLI, Config, and Operations: Logic and Data In/Out

This document describes the command-line interface, configuration loading, healthcheck, and diagnostics export. Every command, every function involved in config and operations, and their inputs and outputs are specified so that the full operational entry points and data flow are clear.

## Role of the CLI and operations layer

The CLI is the only user-facing entry point to the application. It provides: `run` (start the interactive app), `calibrate` (run the calibration wizard), `bom` (print BOM from CSV), `healthcheck` (verify camera and print FPS/temp), and `export-diagnostics` (bundle system info and config for bug reports). Config loading is shared: the CLI and the app both need a merged app config (app.yaml + profile). Operations do not run the main pipeline; they either start it (run, calibrate), print data (bom), or perform one-off checks and file output (healthcheck, export-diagnostics).

## Module and entry point

**Module:** `smartpi.cli`  
**Entry point:** `smartpi.cli:main` (script name `smartpi` via pyproject.toml).  
**Framework:** Click. `main()` is a click group; subcommands are `run`, `calibrate`, `bom`, `export-diagnostics`, `healthcheck`.

---

## Config loading: `_load_app_config(config_dir)`

**Purpose:** Load and merge app config from app.yaml and the selected profile so that one dict contains camera_index, resolution, detector, threshold, blur, and any profile overrides.

**Inputs:** `config_dir` (str): path to the config directory, default `"configs"`.

**Outputs:** Dict. Keys include at least: `camera_index` (int), `resolution` (list of two ints [width, height]), `detector` (str "ir" or "bright"), `threshold` (int). If app.yaml exists and specifies a profile and that profile file exists, the profile dict is merged (profile keys override app keys; key "profile" is removed from the profile before merge so it does not overwrite the profile name). If app.yaml is missing, return default: `{"camera_index": 0, "resolution": [640, 480], "detector": "bright", "threshold": 200}`.

**Logic:** Path(config_dir) / "app.yaml". If not exists, return the default dict. Else open and yaml.safe_load; if None or empty, treat as {}. Read `profile_name = app.get("profile", "classroom")`. Path(config_dir) / "profiles" / f"{profile_name}.yaml". If that file exists, load it, pop "profile" if present, then app = {**app, **profile}. Return app.

**Data contract:** Callers (run, healthcheck, and indirectly the app and wizard) get one dict. No calibration data is loaded here; calibration is loaded separately by the app or wizard from config_dir/calibration.yaml.

---

## Command: `main()` (group)

**Purpose:** Click group; no behavior except to register subcommands and version option.

**Inputs:** Invoked by Click when user runs `smartpi` or `smartpi --version`.  
**Outputs:** None (Click dispatches to subcommand or shows version).

---

## Command: `run(fullscreen, config_dir)`

**Purpose:** Start the interactive projection app.

**Inputs:**  
- `fullscreen` (bool): from `--fullscreen` flag.  
- `config_dir`: from `--config-dir`, default "configs", must be an existing path (file_okay=False).

**Outputs:** None. Does not return until the app exits. Raises SystemExit(1) on ImportError (e.g. renderer not available).

**Logic:** Try import `run_app` from smartpi.renderer.pygame_app; call `run_app(fullscreen=fullscreen, config_dir=config_dir)`. On ImportError, print message to stderr and raise SystemExit(1). So config is not loaded in the CLI for run; the app loads it inside run_app via _load_config. The CLI only passes config_dir.

---

## Command: `calibrate(config_dir)`

**Purpose:** Run the calibration wizard.

**Inputs:** `config_dir`: from `--config-dir`, default "configs", must exist.

**Outputs:** None. Returns when the wizard exits. Raises SystemExit(1) on ImportError.

**Logic:** Try import `run_wizard` from smartpi.ui.calibration_wizard; call `run_wizard(config_dir=config_dir)`. On ImportError, print and SystemExit(1). The wizard loads its own config and writes calibration.yaml; the CLI does not read or write config.

---

## Command: `bom(repo, pen)`

**Purpose:** Print the main BOM (and optionally the IR pen BOM) from the repo’s CSV files to stdout. Useful for ordering parts or checking the bill of materials.

**Inputs:**  
- `repo` (str): path to the repository root, from `--repo`, default `"."`.  
- `pen` (bool): from `--pen` flag; if True, also print the IR pen BOM lines.

**Outputs:** Echoes BOM lines to stdout. Exits with code 1 if the main BOM file is missing.

**Logic:** Resolve repo path; find main BOM CSV (e.g. under repo, per project convention). If main BOM file is missing, print error and SystemExit(1). Else read and echo each line to stdout. If `pen` is True, find and echo IR pen BOM lines from the repo’s pen BOM CSV. No config or calibration is read.

---

## Command: `export_diagnostics(output, config_dir, no_config)`

**Purpose:** Bundle system info and optionally config (excluding calibration and secrets) into a tarball for bug reports.

**Inputs:**  
- `output` (str): output path for the .tar.gz file, default "diagnostics_bundle.tar.gz".  
- `config_dir`: path to config directory, default "configs".  
- `no_config` (bool): if True, do not include config files in the bundle.

**Outputs:** Prints "Diagnostics written to {path}" and exits. The path is the resolved path returned by bundle_diagnostics.

**Logic:** Import `bundle_diagnostics` from smartpi.core.diagnostics. Call `path = bundle_diagnostics(output, include_config=not no_config, config_dir=config_dir)`. Echo the path. So the CLI delegates to the diagnostics module; see below for bundle_diagnostics I/O.

---

## Command: `healthcheck(config_dir)`

**Purpose:** Verify that the camera is detectable and measure FPS (and optionally CPU temperature on Pi).

**Inputs:** `config_dir`: from `--config-dir", default "configs".

**Outputs:** Prints to stdout: "PASS: Camera detected." or "FAIL: Camera not detected." (and exits with code 1 on failure); resolution; FPS; optionally "CPU temp: X.X C". No return value.

**Logic:** (1) Load app config: `app_config = _load_app_config(config_dir)`. (2) Get camera_index and resolution (w, h) from config with defaults. (3) Open cv2.VideoCapture(cam_index), set width and height. If not opened, echo FAIL and SystemExit(1). (4) Create FPSCounter(window_size=30), read 30 frames (tick each), release camera. (5) Echo PASS, resolution, FPS. (6) Try read /sys/class/thermal/thermal_zone0/temp, convert to Celsius, echo; on exception ignore. So healthcheck uses the same config as the app to decide which camera and resolution to test; it does not run the full app or calibration.

---

## Diagnostics: `get_system_info()` and `bundle_diagnostics(...)`

**Module:** `smartpi.core.diagnostics`

**get_system_info():**  
- **Inputs:** None.  
- **Outputs:** Dict[str, str] with keys: "platform" (platform.platform()), "python" (platform.python_version()), "processor" (platform.processor() or "unknown").  
- **Logic:** Call platform module and return the dict. Used inside bundle_diagnostics to write system_info.txt into the tarball.

**bundle_diagnostics(output_path, include_config, config_dir):**  
- **Inputs:** output_path (str or Path), include_config (bool), config_dir (str or Path, default "configs").  
- **Outputs:** Resolved Path to the created .tar.gz file.  
- **Logic:** (1) Ensure output_path parent exists. (2) Open tarfile in write gzip mode. (3) Build system info dict, add "timestamp" (UTC ISO), write to a temp file system_info.txt, add to tar with arcname "system_info.txt", delete temp file. (4) If include_config True and config_dir exists, rglob all files under config_dir; for each file, if "calibration.yaml" not in path, add to tar with arcname "config/{relative_path}". (5) Return output_path.resolve(). So calibration is never included; app.yaml and profiles are included when include_config is True. No secrets stripping beyond excluding calibration; callers should not put secrets in app.yaml or profiles.

---

## Shell scripts (scripts/)

The following scripts wrap CLI commands or print setup instructions. They are invoked from the repo root (or change directory to repo root first). **Data in:** command-line arguments when documented below. **Data out:** exit code 0 on success; script output to stdout/stderr; no return value to callers.

| Script | Purpose | Inputs | Outputs / side effects |
|--------|---------|--------|------------------------|
| **install_pi.sh** | Install Python dependencies (and optionally point to systemd). | None (no args). | Runs `pip install -r requirements.txt`; echoes optional note to copy systemd service. Exit 0. Does not run `pip install -e .`; for editable install use the build guide. |
| **healthcheck.sh** | Run display and camera health checks. | None. | Changes to repo root; runs `python3 -m smartpi.cli healthcheck`; prints display dimensions (if xdpyinfo present) and camera PASS/FAIL, FPS, CPU temp. Exit 0 on success; CLI may exit 1 if camera fails. |
| **run_demo.sh** | Start the interactive app. | All args passed through (`"$@"`). | `exec python3 -m smartpi.cli run "$@"` (e.g. `--fullscreen`, `--config-dir`). Does not return until app exits. |
| **calibrate.sh** | Run the calibration wizard. | All args passed through. | `exec python3 -m smartpi.cli calibrate "$@"`. Does not return until wizard exits. |
| **enable_kiosk.sh** | Print kiosk setup instructions; does not modify the system. | None. | Echoes message to use systemd or autostart .desktop under `src/smartpi/services/`. Exit 0. Does not copy files or enable services. |
| **export_diagnostics.sh** | Bundle diagnostics for bug reports. | Optional first arg: output path (default `diagnostics_bundle.tar.gz`). | `exec python3 -m smartpi.cli export-diagnostics -o "$OUTPUT"`. Writes .tar.gz; echoes path. |

See [02_build_guide.md](../02_build_guide.md) for when to run each script.

---

## Summary: data in and out

| Function / command     | Data in                    | Data out / side effect              |
|------------------------|----------------------------|-------------------------------------|
| _load_app_config       | config_dir                 | dict (app + profile)                 |
| main                   | (Click argv)               | dispatch or version                 |
| run                    | fullscreen, config_dir     | None; runs run_app                  |
| calibrate              | config_dir                 | None; runs run_wizard                |
| bom                    | repo, pen                  | Echo BOM lines (and optional pen BOM); exit 1 if main BOM missing |
| export_diagnostics     | output, config_dir, no_config | Echo path; writes .tar.gz       |
| healthcheck            | config_dir                 | Echo PASS/FAIL, FPS, temp           |
| get_system_info        | (none)                     | dict                                |
| bundle_diagnostics     | output_path, include_config, config_dir | Path to tarball             |

Together with the previous technical documents, this completes the function-level and data-flow documentation for the Smart Pi system in order of services, functionality, and complete data input and output throughout the full pipeline.

Last updated: 2026-03-04
