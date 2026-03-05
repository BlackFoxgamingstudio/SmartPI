# Safety and Power

Basic safety and power notes for running the Smart Pi setup. For **classroom deployment**, the design follows "Engineered for Classroom Safety" principles below.

## Classroom safety (ports-only, isolated power, low-voltage only)

- **Ports-only integration:** Zero invasive soldering to the projector's internal mains power. All connections use standard **external VGA, USB, and 3.5mm** ports only.
- **Isolated power:** The Raspberry Pi runs entirely on its own **fused 5V/5A USB-C** power supply (separate from the projector).
- **Low-voltage student tasks:** Soldering is strictly limited to **low-voltage, battery-powered IR pens** in supervised bench settings. No mains or projector internals.
- **Projector control:** Safe power and input management via **RS-232C (ESC/VP21) or PJLink over LAN**, avoiding the need to open the projector chassis.

## Power

- Use a **rated power supply** for the Raspberry Pi (e.g. official 5 V 3 A for Pi 4). Undervoltage can cause instability and SD corruption.
- **Projector:** Use the manufacturer’s power cable and avoid overloading outlets. Many projectors draw significant current when the lamp is on.
- **Cables:** Route cables so they are not a trip hazard; avoid pinching or stretching.

## Heat

- **Pi:** Ensure adequate cooling (heatsink and/or fan) under sustained load. Thermal throttling will reduce FPS and responsiveness.
- **Projector:** Keep vents clear; do not block airflow. Allow cooldown before moving.
- **Enclosure:** If using an enclosure, provide ventilation so the Pi and any electronics do not overheat.

## Laser pointer (if used)

- Do **not** point a laser at people, eyes, or reflective surfaces. Use only as a pointer on the projection surface.
- Prefer **class 1 or 2** lasers for demos; follow local regulations.

## General

- This project is provided as-is. Users are responsible for safe wiring, power, and use of hardware. See [LICENSE](../LICENSE).

Last updated: 2026-03-04
