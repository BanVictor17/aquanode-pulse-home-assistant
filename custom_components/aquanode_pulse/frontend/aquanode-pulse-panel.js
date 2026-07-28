const TRANSLATIONS = {
  ro: {
    subtitle: "Monitorizare locală a alimentării",
    notReady: "AquaNode Pulse se inițializează…",
    noDevices: "Niciun produs AquaNode Pulse configurat.",
    powerOn: "Curentul este pornit",
    noContact: "Fără legătură",
    noContactHint: "Poate fi pana de curent sau rețeaua. Îți spunem exact când revine.",
    connectedFor: "conectat de",
    lastInterruption: "Ultima întrerupere",
    never: "Nicio întrerupere înregistrată",
    causePower: "Pană de curent",
    causeNetwork: "Problemă de rețea",
    causeUnknown: "Cauză necunoscută",
    causePowerWhy: "Placa a repornit, deci chiar a lipsit curentul.",
    causeNetworkWhy: "Placa a rămas alimentată, deci curentul nu a lipsit.",
    causeUnknownWhy: "Nu există dovezi suficiente pentru a numi cauza.",
    lasted: "a durat",
    ended: "s-a încheiat",
    voltage: "Tensiune",
    signal: "Semnal Wi-Fi",
    internet: "Internet",
    uptime: "Funcționează de",
    firmware: "Firmware",
    serial: "Serie",
    yes: "conectat",
    no: "deconectat",
    notCalibrated: "necalibrat",
    ago: "acum",
    seconds: "s",
    minutes: "min",
    hours: "h",
    days: "z",
  },
  en: {
    subtitle: "Local power monitoring",
    notReady: "AquaNode Pulse is starting…",
    noDevices: "No AquaNode Pulse is configured.",
    powerOn: "Power is on",
    noContact: "No contact",
    noContactHint: "This is either the power or the network. You will be told which when it returns.",
    connectedFor: "connected for",
    lastInterruption: "Last interruption",
    never: "No interruption recorded",
    causePower: "Power cut",
    causeNetwork: "Network problem",
    causeUnknown: "Cause unknown",
    causePowerWhy: "The board restarted, so the power really was off.",
    causeNetworkWhy: "The board stayed powered, so the power was never off.",
    causeUnknownWhy: "There is not enough evidence to name the cause.",
    lasted: "lasted",
    ended: "ended",
    voltage: "Voltage",
    signal: "Wi-Fi signal",
    internet: "Internet",
    uptime: "Up for",
    firmware: "Firmware",
    serial: "Serial",
    yes: "connected",
    no: "disconnected",
    notCalibrated: "not calibrated",
    ago: "",
    seconds: "s",
    minutes: "min",
    hours: "h",
    days: "d",
  },
};

const UNAVAILABLE = new Set(["unavailable", "unknown", ""]);

function duration(seconds, t) {
  const value = Number(seconds);
  if (!Number.isFinite(value) || value < 0) return "-";
  if (value < 90) return `${Math.round(value)} ${t.seconds}`;
  if (value < 5400) return `${Math.round(value / 60)} ${t.minutes}`;
  if (value < 172800) return `${Math.round(value / 3600)} ${t.hours}`;
  return `${Math.round(value / 86400)} ${t.days}`;
}

function since(isoString, t) {
  const when = Date.parse(isoString);
  if (Number.isNaN(when)) return "-";
  return `${t.ago} ${duration((Date.now() - when) / 1000, t)}`.trim();
}

class AquaNodePulsePanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._hass = null;
  }

  set hass(value) {
    this._hass = value;
    this.render();
  }

  set narrow(value) {
    this._narrow = value;
  }

  get language() {
    return this._hass?.language === "ro" ? "ro" : "en";
  }

  // Entities carry their own grouping key, so the panel needs neither the
  // device registry nor a websocket round trip to know which board is which.
  devices() {
    const groups = new Map();
    for (const state of Object.values(this._hass.states)) {
      const serial = state.attributes?.aquanode_serial;
      if (!state.attributes?.aquanode_pulse || !serial) continue;
      if (!groups.has(serial)) {
        groups.set(serial, { serial, name: state.attributes.aquanode_name, metrics: new Map() });
      }
      groups.get(serial).metrics.set(state.attributes.aquanode_metric, state);
    }
    return [...groups.values()].sort((a, b) => a.name.localeCompare(b.name));
  }

  card(device, t) {
    const metric = (key) => device.metrics.get(key);
    const value = (key) => {
      const state = metric(key);
      return state && !UNAVAILABLE.has(state.state) ? state.state : null;
    };

    // Every entity of a board goes unavailable while the board is away, which
    // is itself the signal that contact has been lost.
    const online = [...device.metrics.values()].some((s) => !UNAVAILABLE.has(s.state));

    const cause = value("last_interruption_cause");
    const causeLabel = {
      power: t.causePower,
      network: t.causeNetwork,
      unknown: t.causeUnknown,
    }[cause];
    const causeWhy = {
      power: t.causePowerWhy,
      network: t.causeNetworkWhy,
      unknown: t.causeUnknownWhy,
    }[cause];

    const voltage = value("voltage");
    const rows = [
      [t.voltage, voltage && Number(voltage) > 0 ? `${Number(voltage).toFixed(1)} V` : t.notCalibrated],
      [t.signal, value("wifi_signal") ? `${value("wifi_signal")} dBm` : "-"],
      [t.internet, metric("cloud_connected")?.state === "on" ? t.yes : t.no],
      [t.uptime, value("uptime") ? duration(value("uptime"), t) : "-"],
      [t.serial, device.serial],
    ];

    return `
      <article class="card ${online ? "" : "offline"}">
        <header>
          <div>
            <h2>${device.name}</h2>
            <p class="big">${online ? t.powerOn : t.noContact}</p>
            <p class="sub">${online ? "" : t.noContactHint}</p>
          </div>
          <span class="dot ${online ? "ok" : "bad"}"></span>
        </header>

        <section class="event ${cause ? `cause-${cause}` : "none"}">
          <span class="eyebrow">${t.lastInterruption}</span>
          ${
            cause
              ? `<p class="headline">${causeLabel}</p>
                 <p class="why">${causeWhy}</p>
                 <p class="meta">
                   ${t.lasted} ${duration(value("last_interruption_duration"), t)}
                   &middot; ${t.ended} ${since(value("last_interruption_ended"), t)}
                 </p>`
              : `<p class="headline quiet">${t.never}</p>`
          }
        </section>

        <dl>
          ${rows.map(([label, text]) => `<div><dt>${label}</dt><dd>${text}</dd></div>`).join("")}
        </dl>
      </article>`;
  }

  render() {
    if (!this.shadowRoot) return;
    const t = TRANSLATIONS[this.language];
    if (!this._hass) {
      this.shadowRoot.innerHTML = `<style>${this.styles}</style><div class="loading">${TRANSLATIONS.ro.notReady}</div>`;
      return;
    }
    const devices = this.devices();
    this.shadowRoot.innerHTML = `
      <style>${this.styles}</style>
      <main>
        <header class="page">
          <h1>AquaNode Pulse</h1>
          <p>${t.subtitle}</p>
        </header>
        ${
          devices.length
            ? `<div class="grid">${devices.map((d) => this.card(d, t)).join("")}</div>`
            : `<div class="loading">${t.noDevices}</div>`
        }
      </main>`;
  }

  get styles() {
    return `
      :host {
        display: block;
        min-height: 100%;
        color: var(--primary-text-color);
        background:
          radial-gradient(circle at 12% 0%, color-mix(in srgb, var(--primary-color) 15%, transparent), transparent 36rem),
          var(--primary-background-color);
      }
      main { padding: clamp(16px, 4vw, 40px); max-width: 1100px; margin: 0 auto; }
      .page h1 { margin: 0; font-size: clamp(1.6rem, 4vw, 2.2rem); letter-spacing: -0.02em; }
      .page p { margin: 4px 0 28px; color: var(--secondary-text-color); }
      .loading { padding: 40px; color: var(--secondary-text-color); }
      .grid { display: grid; gap: 20px; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); }
      .card {
        border: 1px solid var(--divider-color);
        border-radius: 20px;
        padding: 22px;
        background: var(--ha-card-background, var(--card-background-color));
        box-shadow: var(--ha-card-box-shadow, 0 8px 28px rgba(0,0,0,.08));
      }
      .card.offline { border-color: color-mix(in srgb, var(--error-color) 45%, var(--divider-color)); }
      .card > header { display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; }
      .card h2 { margin: 0; font-size: 1.05rem; color: var(--secondary-text-color); font-weight: 600; }
      .big { margin: 6px 0 0; font-size: 1.5rem; font-weight: 700; letter-spacing: -0.01em; }
      .sub { margin: 6px 0 0; color: var(--secondary-text-color); font-size: .86rem; max-width: 34ch; }
      .dot { width: 12px; height: 12px; border-radius: 50%; flex: none; margin-top: 6px; }
      .dot.ok { background: var(--success-color, #2e7d32); }
      .dot.bad { background: var(--error-color, #c62828); }
      .event {
        margin: 20px 0 4px;
        padding: 16px;
        border-radius: 14px;
        background: color-mix(in srgb, var(--primary-background-color) 80%, transparent);
        border-left: 4px solid var(--divider-color);
      }
      .event.cause-power { border-left-color: var(--error-color, #c62828); }
      .event.cause-network { border-left-color: var(--warning-color, #ef6c00); }
      .eyebrow {
        font-size: .68rem; letter-spacing: .12em; text-transform: uppercase;
        color: var(--secondary-text-color);
      }
      .headline { margin: 6px 0 0; font-size: 1.05rem; font-weight: 650; }
      .headline.quiet { font-weight: 500; color: var(--secondary-text-color); }
      .why { margin: 4px 0 0; font-size: .86rem; color: var(--secondary-text-color); }
      .meta { margin: 8px 0 0; font-size: .8rem; color: var(--secondary-text-color); }
      dl { display: grid; gap: 1px; margin: 18px 0 0; background: var(--divider-color); border-radius: 12px; overflow: hidden; }
      dl > div {
        display: flex; justify-content: space-between; gap: 12px;
        padding: 10px 14px; background: var(--ha-card-background, var(--card-background-color));
      }
      dt { color: var(--secondary-text-color); font-size: .85rem; }
      dd { margin: 0; font-size: .85rem; font-variant-numeric: tabular-nums; }
      @media (prefers-reduced-motion: no-preference) { .card { transition: border-color .2s ease; } }
    `;
  }
}

if (!customElements.get("aquanode-pulse-panel")) {
  customElements.define("aquanode-pulse-panel", AquaNodePulsePanel);
}
