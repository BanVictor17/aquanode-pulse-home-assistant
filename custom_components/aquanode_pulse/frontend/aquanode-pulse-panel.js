const COPY = {
  ro: {
    local: "LOCAL",
    subtitle: "Monitorizarea alimentării, direct în Home Assistant",
    active: "Monitorizare activă",
    activeHint: "Locuința rămâne sub observație.",
    devicesOnline: (online, total) => `${online} din ${total} dispozitive sunt conectate.`,
    noDevices: "Niciun dispozitiv AquaNode Pulse configurat.",
    noDevicesHint: "Adaugă integrarea din Setări, Dispozitive și servicii.",
    powerOn: "Curentul este pornit",
    noContact: "Fără legătură",
    possibleOutage: "Poate fi o pană de curent sau o problemă de rețea.",
    connectedFor: "conectat de",
    offlineFor: "fără legătură de",
    status: "Stare",
    voltage: "Tensiune",
    device: "Dispozitiv",
    systemOnline: "Sistem online",
    connectionLost: "Legătură întreruptă",
    activity: "Activitate",
    powerOutages: "Întreruperi de curent",
    chartHint: "Sunt incluse doar penele de curent confirmate.",
    journal: "Jurnal",
    latestEvents: "Ultimele evenimente",
    noEvents: "Niciun eveniment înregistrat încă.",
    savedLocally: "Istoricul este salvat local în Home Assistant.",
    clearHistory: "Șterge evenimentele",
    voltageAtOutlet: "Tensiune în priză",
    lastVoltageAt: "Ultima tensiune detectată",
    measuredNow: "Actualizată acum",
    trend: "Evoluție",
    voltageHistory: "Istoricul tensiunii",
    voltageChartHint: "Minimul, media și maximul sunt salvate local.",
    lowVoltageProtection: "Protecție",
    lowVoltageAlerts: "Alerte de tensiune",
    minimumLimit: "Limită minimă",
    changeLimit: "Modifică limita",
    noVoltageIncidents: "Nicio scădere sub limită în acest interval.",
    management: "Administrare",
    renameDevice: "Redenumește dispozitivul",
    renameHint: "Numele este salvat local în Home Assistant.",
    notifications: "Notificări Home Assistant",
    notificationsHint: "Apar automat în centrul de notificări Home Assistant.",
    routerOnUps: "Router protejat prin UPS",
    routerOnUpsHint: "Activează doar dacă routerul, Home Assistant și rețeaua locală rămân alimentate. Lipsa Pulse este raportată imediat ca pană și verificată la revenire.",
    notificationDelay: "Timp minim pentru notificări",
    notificationDelayHint: "Incidentele mai scurte rămân în jurnal, fără notificare.",
    phoneNotifications: "Notificări pe telefon",
    phoneNotificationsHint: "Activează notificările push cu automatizarea pregătită.",
    testNotification: "Trimite o notificare de test",
    testNotificationHint: "Verifică imediat centrul de notificări Home Assistant.",
    access: "Acces și permisiuni",
    accessHint: "Accesul este administrat de utilizatorii Home Assistant.",
    idleLed: "LED albastru în repaus",
    idleLedHint: "Semnalele de configurare și eroare rămân active.",
    calibrate: "Calibrează tensiunea",
    calibrateHint: "Introdu valoarea măsurată simultan cu un multimetru true-RMS.",
    resetCalibration: "Șterge calibrarea",
    identify: "Identifică dispozitivul",
    identifyHint: "LED-ul va clipi pentru a-l putea găsi.",
    restart: "Repornește dispozitivul",
    diagnostics: "Diagnostic",
    diagnosticLogging: "Diagnostic citire locală",
    diagnosticLoggingHint: "Activează temporar detalii despre timeouturi în jurnalul Home Assistant.",
    deviceInformation: "Informații dispozitiv",
    wifiSignal: "Semnal Wi-Fi",
    lastSignal: "Ultimul semnal primit",
    lastLocalResponse: "Ultimul răspuns local",
    filteredPollGaps: "Pauze locale filtrate",
    lastPollIssue: "Ultima eroare",
    noPollIssues: "Nicio problemă detectată",
    uptime: "Timp de funcționare",
    lastConnection: "Ultima reconectare",
    reconnectDuration: "Durata ultimei întreruperi",
    firmware: "Versiune firmware",
    bootCount: "Porniri înregistrate",
    freeMemory: "Memorie disponibilă",
    ipAddress: "Adresă IP",
    serial: "Număr de serie",
    cloud: "AquaNode Cloud",
    calibration: "Calibrare",
    calibrated: "Calibrat",
    calibrationRequired: "Necesară",
    sensorMissing: "Modul nedetectat",
    signalClipped: "Semnal saturat",
    connected: "Conectat",
    disconnected: "Deconectat",
    on: "Pornit",
    off: "Oprit",
    unavailable: "Indisponibil",
    outage: "Pană de curent",
    network: "Problemă de rețea",
    unknown: "Cauză necunoscută",
    maintenance: "Repornire planificată",
    voltageIncident: "Tensiune scăzută",
    ongoing: "În desfășurare",
    started: "A început",
    ended: "S-a încheiat",
    lasted: "Durată",
    minimum: "Minim",
    average: "Medie",
    maximum: "Maxim",
    threshold: "Limită",
    restoredAt: "A revenit la",
    outagesInPeriod: (count) => count === 1 ? "1 pană în interval" : `${count} pene în interval`,
    noVoltageData: "Nu există încă suficiente valori salvate.",
    loading: "Se încarcă…",
    loadFailed: "Istoricul nu a putut fi încărcat.",
    cancel: "Renunță",
    save: "Salvează",
    confirm: "Confirmă",
    valueVolts: "Valoare în volți",
    valueSeconds: "Valoare în secunde",
    valueName: "Numele dispozitivului",
    calibrateTitle: "Calibrare tensiune",
    calibrateBody: "Măsoară acum aceeași priză cu un aparat true-RMS sigur. Nu modifica potențiometrul după calibrare.",
    restartTitle: "Repornești dispozitivul?",
    restartBody: "Întreruperea planificată va fi salvată, dar nu va produce o alertă de pană.",
    resetTitle: "Ștergi calibrarea?",
    resetBody: "Tensiunea nu va mai fi afișată până la o nouă calibrare.",
    clearTitle: "Ștergi jurnalul?",
    clearBody: "Evenimentele încheiate vor fi șterse definitiv. Incidentele active și graficele de tensiune rămân păstrate.",
    done: "Modificarea a fost trimisă.",
    error: "Operația nu a reușit. Verifică dacă dispozitivul este conectat.",
    phoneTitle: "Notificări push pe telefon",
    phoneIntro: "Notificările din Home Assistant sunt deja active. Pentru alerte push pe telefon:",
    phoneSteps: [
      "Instalează aplicația Home Assistant pe telefon și activează notificările.",
      "Importă blueprint-ul AquaNode Pulse folosind butonul de mai jos.",
      "Creează automatizarea, alege dispozitivul Pulse și serviciul telefonului tău.",
      "Salvează automatizarea. Alertele locale și cele mobile vor funcționa independent de AquaNode Cloud.",
    ],
    importBlueprint: "Importă automatizarea",
    accessTitle: "Acces prin Home Assistant",
    accessBody: "AquaNode Pulse respectă utilizatorii și permisiunile instanței Home Assistant. Pentru a oferi sau retrage acces, folosește Setări, Persoane, apoi Utilizatori. Nu este necesar un cont AquaNode Cloud.",
    close: "Închide",
    notAvailable: "Această comandă nu este disponibilă pentru entitatea curentă.",
    day: "24h",
    week: "7 zile",
    month: "30 zile",
    year: "1 an",
  },
  en: {
    local: "LOCAL",
    subtitle: "Power monitoring, directly in Home Assistant",
    active: "Monitoring active",
    activeHint: "Your property remains under observation.",
    devicesOnline: (online, total) => `${online} of ${total} devices are connected.`,
    noDevices: "No AquaNode Pulse device is configured.",
    noDevicesHint: "Add the integration from Settings, Devices & services.",
    powerOn: "Power is on",
    noContact: "No connection",
    possibleOutage: "This may be a power outage or a network problem.",
    connectedFor: "connected for",
    offlineFor: "offline for",
    status: "Status",
    voltage: "Voltage",
    device: "Device",
    systemOnline: "System online",
    connectionLost: "Connection lost",
    activity: "Activity",
    powerOutages: "Power outages",
    chartHint: "Only confirmed power outages are included.",
    journal: "Journal",
    latestEvents: "Latest events",
    noEvents: "No events have been recorded yet.",
    savedLocally: "History is stored locally in Home Assistant.",
    clearHistory: "Clear events",
    voltageAtOutlet: "Mains voltage",
    lastVoltageAt: "Last voltage detected",
    measuredNow: "Updated now",
    trend: "Trend",
    voltageHistory: "Voltage history",
    voltageChartHint: "Minimum, average and maximum values are stored locally.",
    lowVoltageProtection: "Protection",
    lowVoltageAlerts: "Voltage alerts",
    minimumLimit: "Minimum limit",
    changeLimit: "Change limit",
    noVoltageIncidents: "No drops below the limit in this period.",
    management: "Management",
    renameDevice: "Rename device",
    renameHint: "The name is stored locally in Home Assistant.",
    notifications: "Home Assistant notifications",
    notificationsHint: "They appear automatically in the Home Assistant notification center.",
    routerOnUps: "Router protected by UPS",
    routerOnUpsHint: "Enable only when the router, Home Assistant and local network stay powered. A missing Pulse is reported immediately as a power outage and checked on reconnect.",
    notificationDelay: "Minimum notification time",
    notificationDelayHint: "Shorter incidents remain in the journal without a notification.",
    phoneNotifications: "Phone notifications",
    phoneNotificationsHint: "Enable push notifications with the prepared automation.",
    testNotification: "Send a test notification",
    testNotificationHint: "Immediately check the Home Assistant notification center.",
    access: "Access and permissions",
    accessHint: "Access is managed by Home Assistant users.",
    idleLed: "Idle blue LED",
    idleLedHint: "Setup and error patterns remain active.",
    calibrate: "Calibrate voltage",
    calibrateHint: "Enter the value measured at the same time with a true-RMS meter.",
    resetCalibration: "Reset calibration",
    identify: "Identify device",
    identifyHint: "The LED will blink so you can find it.",
    restart: "Restart device",
    diagnostics: "Diagnostics",
    diagnosticLogging: "Local polling diagnostics",
    diagnosticLoggingHint: "Temporarily add timeout details to the Home Assistant log.",
    deviceInformation: "Device information",
    wifiSignal: "Wi-Fi signal",
    lastSignal: "Last signal received",
    lastLocalResponse: "Last local response",
    filteredPollGaps: "Filtered local gaps",
    lastPollIssue: "Last issue",
    noPollIssues: "No issue detected",
    uptime: "Uptime",
    lastConnection: "Last reconnection",
    reconnectDuration: "Last interruption duration",
    firmware: "Firmware version",
    bootCount: "Recorded boots",
    freeMemory: "Available memory",
    ipAddress: "IP address",
    serial: "Serial number",
    cloud: "AquaNode Cloud",
    calibration: "Calibration",
    calibrated: "Calibrated",
    calibrationRequired: "Required",
    sensorMissing: "Module not detected",
    signalClipped: "Signal clipped",
    connected: "Connected",
    disconnected: "Disconnected",
    on: "On",
    off: "Off",
    unavailable: "Unavailable",
    outage: "Power outage",
    network: "Network problem",
    unknown: "Cause unknown",
    maintenance: "Planned restart",
    voltageIncident: "Low voltage",
    ongoing: "Ongoing",
    started: "Started",
    ended: "Ended",
    lasted: "Duration",
    minimum: "Minimum",
    average: "Average",
    maximum: "Maximum",
    threshold: "Limit",
    restoredAt: "Recovered to",
    outagesInPeriod: (count) => count === 1 ? "1 outage in period" : `${count} outages in period`,
    noVoltageData: "There are not enough saved values yet.",
    loading: "Loading…",
    loadFailed: "History could not be loaded.",
    cancel: "Cancel",
    save: "Save",
    confirm: "Confirm",
    valueVolts: "Value in volts",
    valueSeconds: "Value in seconds",
    valueName: "Device name",
    calibrateTitle: "Voltage calibration",
    calibrateBody: "Measure the same outlet now with a safe true-RMS meter. Do not move the potentiometer after calibration.",
    restartTitle: "Restart the device?",
    restartBody: "The planned interruption will be saved, but it will not create an outage alert.",
    resetTitle: "Reset calibration?",
    resetBody: "Voltage will no longer be shown until it is calibrated again.",
    clearTitle: "Clear the journal?",
    clearBody: "Completed events will be permanently removed. Active incidents and voltage graphs will remain saved.",
    done: "The change was sent.",
    error: "The operation failed. Check that the device is connected.",
    phoneTitle: "Phone push notifications",
    phoneIntro: "Home Assistant notifications are already active. For phone push alerts:",
    phoneSteps: [
      "Install the Home Assistant app on the phone and enable notifications.",
      "Import the AquaNode Pulse blueprint using the button below.",
      "Create the automation, select the Pulse and your phone notification service.",
      "Save the automation. Local and mobile alerts work independently of AquaNode Cloud.",
    ],
    importBlueprint: "Import automation",
    accessTitle: "Access through Home Assistant",
    accessBody: "AquaNode Pulse follows the users and permissions of this Home Assistant instance. To grant or revoke access, use Settings, People, then Users. An AquaNode Cloud account is not required.",
    close: "Close",
    notAvailable: "This command is not available for the current entity.",
    day: "24h",
    week: "7 days",
    month: "30 days",
    year: "1 year",
  },
};

const ICONS = {
  arrow: '<path d="m15 18-6-6 6-6"/>',
  bell: '<path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"/><path d="M10 21h4"/>',
  bolt: '<path d="m13 2-8 12h7l-1 8 8-12h-7z"/>',
  chart: '<path d="M4 19V9m5 10V5m6 14v-7m5 7V8"/>',
  check: '<path d="m5 12 4 4L19 6"/>',
  chevron: '<path d="m9 18 6-6-6-6"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  cloud: '<path d="M17.5 19H6a4 4 0 0 1-.5-8A6.5 6.5 0 0 1 18 9.5 4.8 4.8 0 0 1 17.5 19Z"/>',
  device: '<rect x="5" y="3" width="14" height="18" rx="3"/><path d="M9 7h6M10 17h4"/>',
  edit: '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4Z"/>',
  history: '<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5M12 7v5l3 2"/>',
  info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7h.01"/>',
  led: '<path d="M9 18h6M10 22h4M8 14a7 7 0 1 1 8 0c-1 .8-1 2-1 2H9s0-1.2-1-2Z"/>',
  phone: '<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
  refresh: '<path d="M20 7v5h-5M4 17v-5h5"/><path d="M6.1 8A7 7 0 0 1 18 6l2 6M18 16a7 7 0 0 1-12 2l-2-6"/>',
  settings: '<path d="M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Z"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-2.8 2.8-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.6v.2h-4V21a1.7 1.7 0 0 0-1-1.6 1.7 1.7 0 0 0-1.9.3l-.1.1L4.2 17l.1-.1a1.7 1.7 0 0 0 .3-1.9A1.7 1.7 0 0 0 3 14H2.8v-4H3a1.7 1.7 0 0 0 1.6-1 1.7 1.7 0 0 0-.3-1.9L4.2 7 7 4.2l.1.1a1.7 1.7 0 0 0 1.9.3A1.7 1.7 0 0 0 10 3V2.8h4V3a1.7 1.7 0 0 0 1 1.6 1.7 1.7 0 0 0 1.9-.3l.1-.1L19.8 7l-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.6 1h.2v4H21a1.7 1.7 0 0 0-1.6 1Z"/>',
  trash: '<path d="M4 7h16M9 7V4h6v3M7 7l1 14h8l1-14M10 11v6M14 11v6"/>',
  users: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
  voltage: '<path d="m13.5 2.5-7 10.5h5l-1 8.5L18 10h-5z"/><path d="M3 20h18"/>',
  wifi: '<path d="M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0M12 20h.01M2 9a14 14 0 0 1 20 0"/>',
};

const PERIODS = ["day", "week", "month", "year"];
const UNAVAILABLE = new Set(["unavailable", "unknown", ""]);
const BLUEPRINT_URL = "https://github.com/BanVictor17/aquanode-pulse-home-assistant/blob/main/blueprints/automation/aquanode_pulse/interruption_alert.yaml";
const BLUEPRINT_IMPORT = `https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=${encodeURIComponent(BLUEPRINT_URL)}`;

function icon(name, className = "") {
  return `<svg class="icon ${className}" viewBox="0 0 24 24" aria-hidden="true">${ICONS[name] || ICONS.info}</svg>`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function validState(state) {
  return state && !UNAVAILABLE.has(String(state.state));
}

function numberState(state) {
  if (!validState(state)) return null;
  const value = Number(state.state);
  return Number.isFinite(value) ? value : null;
}

// The uptime sensor declares suggested_unit_of_measurement=HOURS, so Home
// Assistant stores its state already converted and the raw number is hours, not
// seconds. Reading it as seconds turned a five hour uptime into "5 sec". The
// unit travels on the state, so use it rather than assuming.
const DURATION_SECONDS = { ms: 0.001, s: 1, sec: 1, min: 60, h: 3_600, d: 86_400 };

function durationSeconds(state) {
  const value = numberState(state);
  if (value === null) return null;
  const unit = String(state?.attributes?.unit_of_measurement || "s").toLowerCase();
  const factor = DURATION_SECONDS[unit];
  return factor === undefined ? null : value * factor;
}

function duration(seconds, language) {
  const value = Number(seconds);
  if (!Number.isFinite(value) || value < 0) return "-";
  if (value < 90) return `${Math.round(value)} sec`;
  if (value < 5_400) return `${Math.round(value / 60)} min`;
  if (value < 172_800) return `${Math.round(value / 3_600)} h`;
  return `${Math.round(value / 86_400)} ${language === "ro" ? "z" : "d"}`;
}

function moment(unixSeconds, language, includeSeconds = false) {
  const value = Number(unixSeconds);
  if (!Number.isFinite(value) || value <= 0) return "-";
  return new Intl.DateTimeFormat(language === "ro" ? "ro-RO" : "en-GB", {
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
    ...(includeSeconds ? { second: "2-digit" } : {}),
  }).format(new Date(value * 1_000));
}

function sinceIso(isoString, language) {
  const value = Date.parse(isoString);
  if (!Number.isFinite(value)) return "-";
  return duration(Math.max(0, (Date.now() - value) / 1_000), language);
}

function formatVoltage(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed > 0 ? `${parsed.toFixed(1)} V` : "-";
}

function wifiQuality(value, language) {
  const rssi = Number(value);
  if (!Number.isFinite(rssi)) return "-";
  const label = rssi >= -55
    ? (language === "ro" ? "Excelent" : "Excellent")
    : rssi >= -67
      ? (language === "ro" ? "Bun" : "Good")
      : rssi >= -75
        ? (language === "ro" ? "Slab" : "Weak")
        : (language === "ro" ? "Foarte slab" : "Very weak");
  return `${Math.round(rssi)} dBm · ${label}`;
}

function bytes(value) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) return "-";
  return `${Math.round(parsed / 1_024)} KB`;
}

function causeLabel(kind, t) {
  return {
    power: t.outage,
    network: t.network,
    unknown: t.unknown,
    maintenance: t.maintenance,
    voltage: t.voltageIncident,
  }[kind] || t.unknown;
}

function pollIssueLabel(kind, language) {
  const labels = language === "ro"
    ? {
        response_timeout: "Răspuns întârziat",
        connection_failed: "Conexiune eșuată",
        invalid_response: "Răspuns invalid",
      }
    : {
        response_timeout: "Delayed response",
        connection_failed: "Connection failed",
        invalid_response: "Invalid response",
      };
  return labels[kind] || "";
}

class AquaNodePulsePanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._hass = null;
    this._screen = { name: "home", serial: null, tab: "general" };
    this._period = { outage: "week", voltage: "day" };
    this._history = new Map();
    this._loading = new Set();
    this._renderSignature = "";
    this._visualSignature = "";
    this._renderPending = false;
    this._toastTimer = null;
    this._tickTimer = null;
    this._historyTimer = null;
    this._narrow = false;
  }

  connectedCallback() {
    if (!this._tickTimer) {
      this._tickTimer = window.setInterval(() => this.updateLive(), 1_000);
    }
    if (!this._historyTimer) {
      this._historyTimer = window.setInterval(() => {
        if (this._screen.name !== "device") return;
        const period = this._screen.tab === "voltage"
          ? this._period.voltage
          : this._period.outage;
        this.loadHistory(this._screen.serial, period, true);
      }, 5_000);
    }
  }

  disconnectedCallback() {
    window.clearInterval(this._tickTimer);
    window.clearInterval(this._historyTimer);
    this._tickTimer = null;
    this._historyTimer = null;
  }

  set hass(value) {
    this._hass = value;
    const structure = this.structureSignature();
    const visual = this.visualSignature();
    if (!this.shadowRoot.innerHTML || structure !== this._renderSignature || visual !== this._visualSignature) {
      // A full render replaces the shadow root, taking any open dialog with it.
      // Values the signature watches do flicker on real hardware: the voltage
      // clipping flag toggles with mains noise, and at one poll a second that
      // shut a dialog before it could be read. Hold the render until the dialog
      // is gone; the live values keep updating underneath it either way.
      if (this.shadowRoot.querySelector(".modal-backdrop")) {
        this._renderPending = true;
        this.updateLive();
        return;
      }
      this.render(true);
      return;
    }
    if (this._renderPending && !this.shadowRoot.querySelector(".modal-backdrop")) {
      this._renderPending = false;
      this.render(true);
      return;
    }
    this.updateLive();
  }

  set narrow(value) {
    this._narrow = value;
    this.toggleAttribute("narrow", Boolean(value));
  }

  get language() {
    return "ro";
  }

  get t() {
    return COPY[this.language];
  }

  devices() {
    if (!this._hass) return [];
    const groups = new Map();
    for (const state of Object.values(this._hass.states)) {
      const attributes = state.attributes || {};
      const serial = attributes.aquanode_serial;
      if (!attributes.aquanode_pulse || !serial) continue;
      if (!groups.has(serial)) {
        groups.set(serial, {
          serial,
          name: attributes.aquanode_name || `AquaNode Pulse ${serial.replace("AP-", "")}`,
          firmware: attributes.aquanode_firmware || "",
          ip: attributes.aquanode_ip || "",
          bootCount: attributes.aquanode_boot_count ?? null,
          freeHeap: attributes.aquanode_free_heap ?? null,
          metrics: new Map(),
        });
      }
      const device = groups.get(serial);
      device.name = attributes.aquanode_name || device.name;
      device.firmware = attributes.aquanode_firmware || device.firmware;
      device.ip = attributes.aquanode_ip || device.ip;
      device.bootCount = attributes.aquanode_boot_count ?? device.bootCount;
      device.freeHeap = attributes.aquanode_free_heap ?? device.freeHeap;
      device.metrics.set(attributes.aquanode_metric, state);
    }
    return [...groups.values()].sort((left, right) => left.name.localeCompare(right.name));
  }

  device(serial = this._screen.serial) {
    return this.devices().find((item) => item.serial === serial) || null;
  }

  metric(device, key) {
    return device?.metrics.get(key) || null;
  }

  value(device, key) {
    const state = this.metric(device, key);
    return validState(state) ? state.state : null;
  }

  isOn(device, key) {
    return this.metric(device, key)?.state === "on";
  }

  isOnline(device) {
    const connection = this.metric(device, "local_connection");
    if (connection) return connection.state === "on";
    return validState(this.metric(device, "uptime"));
  }

  structureSignature() {
    const devices = this.devices();
    return JSON.stringify({
      language: this.language,
      screen: this._screen,
      devices: devices.map((device) => [
        device.serial,
        device.name,
        [...device.metrics.keys()].sort(),
      ]),
    });
  }

  visualSignature() {
    return JSON.stringify(this.devices().map((device) => ({
      serial: device.serial,
      online: this.isOnline(device),
      low: this.isOn(device, "low_voltage"),
      sensorProblem: this.isOn(device, "voltage_sensor_problem"),
      clipped: this.isOn(device, "voltage_clipped"),
      calibration: this.isOn(device, "calibration_required"),
      led: this.isOn(device, "idle_led"),
      notifications: this.isOn(device, "automatic_notifications"),
      routerOnUps: this.isOn(device, "router_on_ups"),
      diagnostics: this.isOn(device, "diagnostic_logging"),
      event: this.metric(device, "last_interruption_ended")?.last_updated || "",
    })));
  }

  historyKey(serial, period) {
    return `${serial}:${period}`;
  }

  history(serial, period) {
    return this._history.get(this.historyKey(serial, period)) || null;
  }

  async loadHistory(serial, period, force = false) {
    if (!this._hass || !serial) return;
    const key = this.historyKey(serial, period);
    if ((!force && this._history.has(key)) || this._loading.has(key)) return;
    this._loading.add(key);
    try {
      const result = await this._hass.connection.sendMessagePromise({
        type: "aquanode_pulse/history",
        serial,
        period,
      });
      this._history.set(key, result);
      this.refreshHistoryView(serial, period, result);
    } catch (error) {
      console.warn("AquaNode Pulse history", error);
      if (!this._history.has(key)) this._history.set(key, { error: true });
    } finally {
      this._loading.delete(key);
    }
  }

  writeSection(node, markup) {
    if (!node || node.dataset.markup === markup) return;
    const expanded = new Set(
      [...node.querySelectorAll("details[open][data-section]")]
        .map((child) => child.dataset.section),
    );
    node.innerHTML = markup;
    node.dataset.markup = markup;
    for (const child of node.querySelectorAll("details[data-section]")) {
      if (expanded.has(child.dataset.section)) child.open = true;
    }
  }

  render(preserveScroll = false) {
    if (!this.shadowRoot || !this._hass) {
      if (this.shadowRoot) {
        this.shadowRoot.innerHTML = `<style>${this.styles}</style><div class="loading">AquaNode Pulse</div>`;
      }
      return;
    }
    const scrollTop = preserveScroll ? window.scrollY : 0;
    const expanded = new Set(
      [...this.shadowRoot.querySelectorAll("details[open][data-section]")]
        .map((node) => node.dataset.section),
    );
    if (this._screen.name === "device" && !this.device()) {
      this._screen = { name: "home", serial: null, tab: "general" };
    }

    this.shadowRoot.innerHTML = `
      <style>${this.styles}</style>
      <div class="shell">
        ${this._screen.name === "home" ? this.renderHome() : this.renderDevice()}
      </div>
      <div class="toast" id="toast" role="status"></div>
      <div id="modalRoot"></div>
    `;
    for (const node of this.shadowRoot.querySelectorAll("details[data-section]")) {
      if (expanded.has(node.dataset.section)) node.open = true;
    }
    this._renderSignature = this.structureSignature();
    this._visualSignature = this.visualSignature();
    this.bind();
    this.updateLive();

    if (preserveScroll) {
      requestAnimationFrame(() => window.scrollTo({ top: scrollTop, behavior: "instant" }));
    } else {
      window.scrollTo({ top: 0, behavior: "instant" });
    }
  }

  brandHeader(title, back = false) {
    return `
      <header class="topbar">
        ${back ? `<button class="icon-button back" data-nav="back" aria-label="Back">${icon("arrow")}</button>` : ""}
        <div class="brand-mark">${icon("bolt", "solid")}</div>
        <div class="titles">
          <span class="brandline">AQUANODE <b>${this.t.local}</b></span>
          <h1>${escapeHtml(title)}</h1>
        </div>
        <div class="live-pill"><span></span><em>${this.t.local}</em></div>
      </header>
    `;
  }

  renderHome() {
    const devices = this.devices();
    const online = devices.filter((device) => this.isOnline(device)).length;
    const allOnline = devices.length > 0 && online === devices.length;
    return `
      ${this.brandHeader("Pulse")}
      <main>
        <section class="home-hero ${allOnline ? "all-ok" : ""}">
          <div>
            <span class="eyebrow">AQUANODE PULSE</span>
            <h2>${this.t.active}</h2>
            <p>${devices.length ? this.t.devicesOnline(online, devices.length) : this.t.activeHint}</p>
          </div>
          <div class="hero-bolt">${icon("bolt", "solid")}</div>
        </section>

        <div class="section-head">
          <div><span class="eyebrow">${this.t.status}</span><h2>${this.language === "ro" ? "Dispozitivele tale" : "Your devices"}</h2></div>
          <span class="count">${devices.length}</span>
        </div>

        ${devices.length
          ? `<div class="device-grid">${devices.map((device) => this.deviceCard(device)).join("")}</div>`
          : `<section class="empty card">
              <div class="empty-icon">${icon("device")}</div>
              <h3>${this.t.noDevices}</h3>
              <p>${this.t.noDevicesHint}</p>
            </section>`}

        <section class="local-note">
          ${icon("check")}
          <div><strong>${this.language === "ro" ? "Funcționare locală" : "Local operation"}</strong>
          <span>${this.language === "ro"
            ? "Valorile, istoricul și comenzile nu depind de AquaNode Cloud."
            : "Values, history and controls do not depend on AquaNode Cloud."}</span></div>
        </section>
      </main>
    `;
  }

  deviceCard(device) {
    const online = this.isOnline(device);
    const voltage = numberState(this.metric(device, "voltage"))
      ?? numberState(this.metric(device, "last_voltage"));
    const uptimeSeconds = durationSeconds(this.metric(device, "uptime"));
    const statusMoment = this.metric(device, "local_connection")?.last_changed;
    return `
      <button class="device-card card ${online ? "online" : "offline"}" data-open-device="${escapeHtml(device.serial)}">
        <span class="rail"></span>
        <span class="device-orb">${icon("bolt", "solid")}</span>
        <span class="device-copy">
          <span class="device-name">${escapeHtml(device.name)}</span>
          <span class="device-state"><i></i><b data-card-state="${escapeHtml(device.serial)}">${online ? this.t.powerOn : this.t.noContact}</b></span>
        </span>
        <span class="device-side">
          <strong data-card-voltage="${escapeHtml(device.serial)}">${formatVoltage(voltage)}</strong>
          ${icon("chevron")}
        </span>
        <span class="device-foot" data-card-meta="${escapeHtml(device.serial)}" data-status-moment="${escapeHtml(statusMoment || "")}">
          ${online ? this.t.connectedFor : this.t.offlineFor} ${
            online && uptimeSeconds !== null
              ? duration(uptimeSeconds, this.language)
              : sinceIso(statusMoment, this.language)
          }
          <i>·</i> ${escapeHtml(device.serial)}
        </span>
      </button>
    `;
  }

  renderDevice() {
    const device = this.device();
    const tab = this._screen.tab;
    const content = tab === "voltage"
      ? this.renderVoltage(device)
      : tab === "settings"
        ? this.renderSettings(device)
        : this.renderGeneral(device);
    return `
      ${this.brandHeader(device.name, true)}
      <main class="device-main">
        ${content}
      </main>
      ${this.deviceTabs(device.serial, tab)}
    `;
  }

  deviceTabs(serial, tab) {
    const items = [
      ["general", "bolt", this.t.status],
      ["voltage", "voltage", this.t.voltage],
      ["settings", "settings", this.t.device],
    ];
    return `
      <nav class="device-tabs" aria-label="${this.t.device}">
        ${items.map(([key, iconName, label]) => `
          <button class="${tab === key ? "on" : ""}" data-device-tab="${key}" data-serial="${escapeHtml(serial)}">
            ${icon(iconName)}<span>${label}</span>
          </button>
        `).join("")}
      </nav>
    `;
  }

  renderGeneral(device) {
    const online = this.isOnline(device);
    const period = this._period.outage;
    const history = this.history(device.serial, period);
    if (!history) this.loadHistory(device.serial, period);
    const events = history?.recent_events || [];
    return `
      <section class="status-hero card ${online ? "ok" : "bad"}" data-status-hero>
        <span class="eyebrow" data-live-status-eyebrow>${online ? this.t.systemOnline : this.t.connectionLost}</span>
        <div class="status-ring">${online ? icon("bolt", "solid") : icon("refresh")}</div>
        <h2>${escapeHtml(device.name)}</h2>
        <strong data-live-power>${online ? this.t.powerOn : this.t.noContact}</strong>
        <p data-live-duration>${this.statusDuration(device)}</p>
        ${online ? "" : `<small>${this.t.possibleOutage}</small>`}
      </section>

      ${this.sectionHead(this.t.activity, this.t.powerOutages)}
      <section class="chart-card card">
        ${this.periodTabs("outage", period)}
        <div class="chart-copy">
          <div><strong data-outage-summary>${history && !history.error ? this.t.outagesInPeriod((history.events || []).filter((item) => item.kind === "power").length) : this.t.loading}</strong>
          <span>${this.t.chartHint}</span></div>
        </div>
        <div data-outage-chart-container>${history?.error ? `<div class="chart-empty">${this.t.loadFailed}</div>` : this.outageChart(history?.events || [], period)}</div>
      </section>

      ${this.sectionHead(this.t.journal, this.t.latestEvents)}
      <section class="journal" data-event-journal>
        ${history
          ? events.length
            ? [...events].reverse().slice(0, 12).map((event) => this.eventRow(event)).join("")
            : `<div class="empty-row card">${this.t.noEvents}</div>`
          : `<div class="empty-row card">${this.t.loading}</div>`}
      </section>
      <div class="journal-actions">
        <span>${icon("check")} ${this.t.savedLocally}</span>
        <button class="text-button danger" data-action="clear-history">${icon("trash")} ${this.t.clearHistory}</button>
      </div>
    `;
  }

  statusDuration(device) {
    const online = this.isOnline(device);
    const state = this.metric(device, "uptime");
    if (online) {
      return `${this.t.connectedFor} ${duration(durationSeconds(state), this.language)}`;
    }
    return `${this.t.offlineFor} ${sinceIso(state?.last_updated, this.language)}`;
  }

  renderVoltage(device) {
    const period = this._period.voltage;
    const history = this.history(device.serial, period);
    if (!history) this.loadHistory(device.serial, period);
    const online = this.isOnline(device);
    const liveVoltage = numberState(this.metric(device, "voltage"));
    const savedVoltage = numberState(this.metric(device, "last_voltage"))
      ?? Number(history?.last_voltage?.value);
    const displayVoltage = online ? liveVoltage : savedVoltage;
    const measuredAt = this.metric(device, "last_voltage")?.attributes?.measured_at;
    const low = this.isOn(device, "low_voltage");
    const threshold = numberState(this.metric(device, "voltage_minimum")) ?? 0;
    const incidents = (history?.recent_events || []).filter((event) => event.kind === "voltage");
    return `
      <section class="voltage-hero card ${low ? "warning" : online && liveVoltage ? "ok" : "neutral"}" data-voltage-hero>
        <span class="eyebrow">${this.t.voltageAtOutlet}</span>
        <strong data-live-voltage>${formatVoltage(displayVoltage)}</strong>
        <p data-live-voltage-state>${online && liveVoltage
          ? this.t.measuredNow
          : `${this.t.lastVoltageAt} ${measuredAt ? moment(Date.parse(measuredAt) / 1_000, this.language, true) : this.t.unavailable}`}</p>
        ${low ? `<div class="warning-pill">${this.t.voltageIncident} · ${formatVoltage(threshold)}</div>` : ""}
      </section>

      ${this.sectionHead(this.t.trend, this.t.voltageHistory)}
      <section class="chart-card voltage-chart-card card">
        ${this.periodTabs("voltage", period)}
        <div data-voltage-chart-container>${history?.error
          ? `<div class="chart-empty">${this.t.loadFailed}</div>`
          : this.voltageChart(history?.voltage || [], threshold)}</div>
        <p class="chart-note">${this.t.voltageChartHint}</p>
      </section>

      ${this.sectionHead(this.t.lowVoltageProtection, this.t.lowVoltageAlerts)}
      <section class="limit-card card">
        <div><span>${this.t.minimumLimit}</span><strong>${threshold > 0 ? formatVoltage(threshold) : this.t.off}</strong></div>
        <p>${this.language === "ro"
          ? "Primești o alertă când tensiunea scade sub limită și încă una când revine stabil."
          : "You receive one alert below the limit and another after voltage returns to normal."}</p>
        <button class="secondary-button" data-action="set-voltage-min">${this.t.changeLimit}</button>
      </section>
      <section class="journal voltage-journal" data-voltage-journal>
        ${incidents.length
          ? [...incidents].reverse().slice(0, 8).map((event) => this.eventRow(event)).join("")
          : `<div class="empty-row card">${this.t.noVoltageIncidents}</div>`}
      </section>
    `;
  }

  renderSettings(device) {
    const threshold = numberState(this.metric(device, "voltage_minimum")) ?? 0;
    const notificationDelay = numberState(this.metric(device, "notification_delay")) ?? 0;
    const calibrated = !this.isOn(device, "calibration_required")
      && numberState(this.metric(device, "voltage")) !== null;
    const calibrationText = this.isOn(device, "voltage_sensor_problem")
      ? this.t.sensorMissing
      : this.isOn(device, "voltage_clipped")
        ? this.t.signalClipped
        : calibrated
          ? this.t.calibrated
          : this.t.calibrationRequired;
    const localConnection = this.metric(device, "local_connection");
    const localDiagnostics = localConnection?.attributes || {};
    const lastPollIssue = pollIssueLabel(
      localDiagnostics.last_poll_issue,
      this.language,
    );
    const lastPollIssueText = lastPollIssue
      ? `${lastPollIssue} · ${moment(localDiagnostics.last_poll_issue_at, this.language, true)}`
      : this.t.noPollIssues;
    const rows = [
      {
        action: "rename-device",
        icon: "edit",
        title: this.t.renameDevice,
        hint: this.t.renameHint,
        value: device.name,
      },
      {
        action: "toggle-notifications",
        icon: "bell",
        title: this.t.notifications,
        hint: this.t.notificationsHint,
        value: this.isOn(device, "automatic_notifications") ? this.t.on : this.t.off,
        toggle: this.isOn(device, "automatic_notifications"),
      },
      {
        action: "set-notification-delay",
        icon: "clock",
        title: this.t.notificationDelay,
        hint: this.t.notificationDelayHint,
        value: `${Math.round(notificationDelay)} sec`,
      },
      {
        action: "toggle-router-on-ups",
        icon: "wifi",
        title: this.t.routerOnUps,
        hint: this.t.routerOnUpsHint,
        value: this.isOn(device, "router_on_ups") ? this.t.on : this.t.off,
        toggle: this.isOn(device, "router_on_ups"),
      },
      {
        action: "phone-help",
        icon: "phone",
        title: this.t.phoneNotifications,
        hint: this.t.phoneNotificationsHint,
        value: "",
      },
      {
        action: "test-notification",
        icon: "bell",
        title: this.t.testNotification,
        hint: this.t.testNotificationHint,
        value: "",
      },
      {
        action: "set-voltage-min",
        icon: "voltage",
        title: this.t.lowVoltageAlerts,
        hint: this.language === "ro" ? "0 V dezactivează alerta." : "0 V disables the alert.",
        value: threshold > 0 ? formatVoltage(threshold) : this.t.off,
      },
      {
        action: "calibrate",
        icon: "settings",
        title: this.t.calibrate,
        hint: this.t.calibrateHint,
        value: calibrationText,
      },
      {
        action: "toggle-led",
        icon: "led",
        title: this.t.idleLed,
        hint: this.t.idleLedHint,
        value: this.isOn(device, "idle_led") ? this.t.on : this.t.off,
        toggle: this.isOn(device, "idle_led"),
      },
      {
        action: "toggle-diagnostic-logging",
        icon: "info",
        title: this.t.diagnosticLogging,
        hint: this.t.diagnosticLoggingHint,
        value: this.isOn(device, "diagnostic_logging") ? this.t.on : this.t.off,
        toggle: this.isOn(device, "diagnostic_logging"),
      },
      {
        action: "access-help",
        icon: "users",
        title: this.t.access,
        hint: this.t.accessHint,
        value: "",
      },
    ];
    return `
      ${this.sectionHead(this.t.management, this.t.device)}
      <section class="settings-rows card">
        ${rows.map((row) => this.settingsRow(row)).join("")}
      </section>

      ${this.sectionHead(this.language === "ro" ? "Acțiuni" : "Actions", this.language === "ro" ? "Comenzi locale" : "Local controls")}
      <section class="settings-rows card">
        ${this.settingsRow({ action: "identify", icon: "led", title: this.t.identify, hint: this.t.identifyHint })}
        ${this.settingsRow({ action: "reset-calibration", icon: "refresh", title: this.t.resetCalibration, hint: this.language === "ro" ? "Elimină factorul salvat în dispozitiv." : "Removes the factor stored on the device." })}
        ${this.settingsRow({ action: "restart", icon: "refresh", title: this.t.restart, hint: this.language === "ro" ? "Repornire controlată, fără alertă falsă de pană." : "Controlled restart without a false outage alert.", danger: true })}
      </section>

      <details class="diagnostics card" data-section="diagnostics">
        <summary>
          <span><small class="eyebrow">${this.t.diagnostics}</small><strong>${this.t.deviceInformation}</strong></span>
          ${icon("chevron")}
        </summary>
        <div class="diagnostic-list">
          ${this.infoRow(this.t.wifiSignal, wifiQuality(this.value(device, "wifi_signal"), this.language), "wifi")}
          ${this.infoRow(this.t.lastSignal, this.isOnline(device) ? this.t.measuredNow : sinceIso(this.metric(device, "uptime")?.last_updated, this.language), "clock")}
          ${this.infoRow(this.t.lastLocalResponse, Number.isFinite(Number(localDiagnostics.last_response_ms)) ? `${Number(localDiagnostics.last_response_ms).toFixed(1)} ms` : this.t.unavailable, "clock")}
          ${this.infoRow(this.t.filteredPollGaps, String(localDiagnostics.filtered_poll_gaps ?? 0), "info")}
          ${this.infoRow(this.t.lastPollIssue, lastPollIssueText, "info")}
          ${this.infoRow(this.t.uptime, duration(durationSeconds(this.metric(device, "uptime")), this.language), "clock")}
          ${this.infoRow(this.t.lastConnection, this.historyLastEnded(device), "history")}
          ${this.infoRow(this.t.reconnectDuration, duration(this.value(device, "last_interruption_duration"), this.language), "clock")}
          ${this.infoRow(this.t.firmware, device.firmware || this.t.unavailable, "device")}
          ${this.infoRow(this.t.bootCount, this.value(device, "boot_count") || device.bootCount || this.t.unavailable, "history")}
          ${this.infoRow(this.t.freeMemory, bytes(this.value(device, "free_heap") || device.freeHeap), "device")}
          ${this.infoRow(this.t.ipAddress, device.ip || this.value(device, "ip_address") || this.t.unavailable, "wifi")}
          ${this.infoRow(this.t.cloud, this.isOn(device, "cloud_connected") ? this.t.connected : this.t.disconnected, "cloud")}
          ${this.infoRow(this.t.calibration, calibrationText, "settings")}
          ${this.infoRow(this.t.serial, device.serial, "info")}
        </div>
      </details>
    `;
  }

  historyLastEnded(device) {
    const value = this.value(device, "last_interruption_ended");
    if (!value) return this.language === "ro" ? "Nicio întrerupere" : "No interruption";
    return moment(Date.parse(value) / 1_000, this.language, true);
  }

  settingsRow({ action, icon: iconName, title, hint = "", value = "", toggle = null, danger = false }) {
    return `
      <button class="settings-row ${danger ? "danger" : ""}" data-action="${action}">
        <span class="row-icon">${icon(iconName)}</span>
        <span class="row-copy"><strong>${title}</strong>${hint ? `<small>${hint}</small>` : ""}</span>
        ${toggle === null
          ? `<span class="row-value">${escapeHtml(value)}</span>${icon("chevron")}`
          : `<span class="toggle ${toggle ? "on" : ""}"><i></i></span>`}
      </button>
    `;
  }

  infoRow(label, value, iconName) {
    return `
      <div class="info-row">
        <span class="row-icon">${icon(iconName)}</span>
        <span>${label}</span>
        <strong>${escapeHtml(value)}</strong>
      </div>
    `;
  }

  sectionHead(eyebrow, title) {
    return `<div class="section-head"><div><span class="eyebrow">${eyebrow}</span><h2>${title}</h2></div></div>`;
  }

  periodTabs(kind, selected) {
    return `
      <div class="period-tabs">
        ${PERIODS.map((period) => `<button class="${selected === period ? "on" : ""}" data-period-kind="${kind}" data-period="${period}">${this.t[period]}</button>`).join("")}
      </div>
    `;
  }

  outageBuckets(events, period) {
    const now = new Date();
    const buckets = [];
    if (period === "day") {
      for (let index = 23; index >= 0; index -= 1) {
        const start = new Date(now);
        start.setMinutes(0, 0, 0);
        start.setHours(start.getHours() - index);
        const end = new Date(start);
        end.setHours(end.getHours() + 1);
        buckets.push({ start, end, label: index % 6 === 0 ? `${String(start.getHours()).padStart(2, "0")}:00` : "" });
      }
    } else if (period === "week" || period === "month") {
      const days = period === "week" ? 7 : 30;
      for (let index = days - 1; index >= 0; index -= 1) {
        const start = new Date(now);
        start.setHours(0, 0, 0, 0);
        start.setDate(start.getDate() - index);
        const end = new Date(start);
        end.setDate(end.getDate() + 1);
        const show = period === "week" || index % 5 === 0 || index === 0;
        buckets.push({ start, end, label: show ? String(start.getDate()) : "" });
      }
    } else {
      for (let index = 11; index >= 0; index -= 1) {
        const start = new Date(now.getFullYear(), now.getMonth() - index, 1);
        const end = new Date(start.getFullYear(), start.getMonth() + 1, 1);
        const label = new Intl.DateTimeFormat(this.language === "ro" ? "ro-RO" : "en-GB", { month: "short" }).format(start);
        buckets.push({ start, end, label });
      }
    }
    for (const bucket of buckets) bucket.count = 0;
    for (const event of events.filter((item) => item.kind === "power")) {
      const at = Number(event.started_at) * 1_000;
      const bucket = buckets.find((item) => at >= item.start.getTime() && at < item.end.getTime());
      if (bucket) bucket.count += 1;
    }
    return buckets;
  }

  outageChart(events, period) {
    const buckets = this.outageBuckets(events, period);
    const width = 360;
    const top = 12;
    const base = 102;
    const slot = width / Math.max(1, buckets.length);
    const max = Math.max(1, ...buckets.map((bucket) => bucket.count));
    const barWidth = Math.max(3, Math.min(20, slot * 0.58));
    const bars = buckets.map((bucket, index) => {
      const height = bucket.count ? Math.max(5, bucket.count / max * 76) : 3;
      const x = index * slot + (slot - barWidth) / 2;
      const y = base - height;
      const label = bucket.label
        ? `<text x="${(index + 0.5) * slot}" y="122">${escapeHtml(bucket.label)}</text>`
        : "";
      return `<rect class="${bucket.count ? "has-value" : ""}" x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${barWidth.toFixed(1)}" height="${height.toFixed(1)}" rx="2"><title>${bucket.count}</title></rect>${label}`;
    }).join("");
    return `<svg class="outage-chart" viewBox="0 0 360 130" role="img"><line x1="0" y1="${base}" x2="${width}" y2="${base}"/>${bars}</svg>`;
  }

  voltageChart(samples, threshold) {
    if (!samples.length) return `<div class="chart-empty">${this.t.noVoltageData}</div>`;
    const width = 360;
    const height = 174;
    const left = 38;
    const right = 8;
    const top = 16;
    const bottom = 30;
    const plotWidth = width - left - right;
    const plotHeight = height - top - bottom;
    const values = samples.flatMap((sample) => [Number(sample.minimum), Number(sample.maximum)]).filter(Number.isFinite);
    if (threshold > 0) values.push(threshold);
    const measuredMin = Math.min(...samples.map((sample) => Number(sample.minimum)));
    const measuredMax = Math.max(...samples.map((sample) => Number(sample.maximum)));
    const weighted = samples.reduce((acc, sample) => {
      const count = Number(sample.count) || 1;
      return { sum: acc.sum + Number(sample.average) * count, count: acc.count + count };
    }, { sum: 0, count: 0 });
    const average = weighted.count ? weighted.sum / weighted.count : 0;
    const padding = Math.max(3, (Math.max(...values) - Math.min(...values)) * 0.18);
    const lower = Math.floor(Math.min(...values) - padding);
    const upper = Math.ceil(Math.max(...values) + padding);
    const from = Number(samples[0].at);
    const to = Math.max(Number(samples.at(-1).at), from + 1);
    const x = (at) => left + (Number(at) - from) / (to - from) * plotWidth;
    const y = (volts) => top + (upper - Number(volts)) / (upper - lower || 1) * plotHeight;
    const averagePath = samples.map((sample, index) => `${index ? "L" : "M"}${x(sample.at).toFixed(1)},${y(sample.average).toFixed(1)}`).join(" ");
    const upperPath = samples.map((sample, index) => `${index ? "L" : "M"}${x(sample.at).toFixed(1)},${y(sample.maximum).toFixed(1)}`).join(" ");
    const lowerPath = [...samples].reverse().map((sample) => `L${x(sample.at).toFixed(1)},${y(sample.minimum).toFixed(1)}`).join(" ");
    const grid = [0, 0.5, 1].map((position) => {
      const value = upper - (upper - lower) * position;
      const yy = y(value);
      return `<line x1="${left}" y1="${yy.toFixed(1)}" x2="${width - right}" y2="${yy.toFixed(1)}"/><text x="${left - 6}" y="${(yy + 3).toFixed(1)}">${Math.round(value)}V</text>`;
    }).join("");
    const thresholdLine = threshold > 0 && threshold >= lower && threshold <= upper
      ? `<line class="threshold" x1="${left}" y1="${y(threshold).toFixed(1)}" x2="${width - right}" y2="${y(threshold).toFixed(1)}"/>`
      : "";
    return `
      <div class="voltage-summary">
        <span><small>${this.t.minimum}</small><strong>${measuredMin.toFixed(1)} V</strong></span>
        <span><small>${this.t.average}</small><strong>${average.toFixed(1)} V</strong></span>
        <span><small>${this.t.maximum}</small><strong>${measuredMax.toFixed(1)} V</strong></span>
      </div>
      <svg class="voltage-chart" viewBox="0 0 ${width} ${height}" role="img">
        <g class="grid-lines">${grid}</g>
        ${thresholdLine}
        <path class="voltage-band" d="${upperPath} ${lowerPath} Z"/>
        <path class="voltage-line" d="${averagePath}"/>
        <text class="time start" x="${left}" y="${height - 7}">${moment(from, this.language)}</text>
        <text class="time end" x="${width - right}" y="${height - 7}">${moment(to, this.language)}</text>
      </svg>
    `;
  }

  eventRow(event) {
    const kind = event.kind || "unknown";
    const ended = Number(event.ended_at);
    const started = Number(event.started_at);
    const status = ended
      ? `${moment(started, this.language, true)} · ${duration(event.duration_seconds, this.language)}`
      : `${moment(started, this.language, true)} · ${this.t.ongoing}`;
    const details = [
      [this.t.started, moment(started, this.language, true)],
      [this.t.ended, ended ? moment(ended, this.language, true) : this.t.ongoing],
      [this.t.lasted, ended ? duration(event.duration_seconds, this.language) : duration(Date.now() / 1_000 - started, this.language)],
    ];
    if (kind === "voltage") {
      details.push(
        [this.t.minimum, formatVoltage(event.minimum_voltage)],
        [this.t.threshold, formatVoltage(event.threshold_voltage)],
      );
      if (event.restored_voltage) details.push([this.t.restoredAt, formatVoltage(event.restored_voltage)]);
    }
    return `
      <details class="event-row ${kind}" data-section="event-${kind}-${started}">
        <summary>
          <span class="event-dot"></span>
          <span class="event-copy"><strong>${causeLabel(kind, this.t)}</strong><small>${status}</small></span>
          ${icon("chevron")}
        </summary>
        <dl>${details.map(([label, value]) => `<div><dt>${label}</dt><dd>${value}</dd></div>`).join("")}</dl>
      </details>
    `;
  }

  refreshHistoryView(serial, period, history) {
    if (
      this._screen.name !== "device"
      || this._screen.serial !== serial
      || !this.shadowRoot
    ) {
      return;
    }
    if (this._screen.tab === "general" && period === this._period.outage) {
      const events = history.events || [];
      const recent = history.recent_events || [];
      const summary = this.shadowRoot.querySelector("[data-outage-summary]");
      const chart = this.shadowRoot.querySelector("[data-outage-chart-container]");
      const journal = this.shadowRoot.querySelector("[data-event-journal]");
      if (summary) {
        summary.textContent = this.t.outagesInPeriod(
          events.filter((item) => item.kind === "power").length,
        );
      }
      this.writeSection(chart, this.outageChart(events, period));
      this.writeSection(
        journal,
        recent.length
          ? [...recent].reverse().slice(0, 12).map((event) => this.eventRow(event)).join("")
          : `<div class="empty-row card">${this.t.noEvents}</div>`,
      );
      return;
    }
    if (this._screen.tab === "voltage" && period === this._period.voltage) {
      const device = this.device(serial);
      const threshold = numberState(this.metric(device, "voltage_minimum")) ?? 0;
      const chart = this.shadowRoot.querySelector("[data-voltage-chart-container]");
      const journal = this.shadowRoot.querySelector("[data-voltage-journal]");
      this.writeSection(chart, this.voltageChart(history.voltage || [], threshold));
      const incidents = (history.recent_events || []).filter(
        (event) => event.kind === "voltage",
      );
      this.writeSection(
        journal,
        incidents.length
          ? [...incidents].reverse().slice(0, 8).map((event) => this.eventRow(event)).join("")
          : `<div class="empty-row card">${this.t.noVoltageIncidents}</div>`,
      );
    }
  }

  bind() {
    for (const button of this.shadowRoot.querySelectorAll("[data-open-device]")) {
      button.addEventListener("click", () => {
        this._screen = { name: "device", serial: button.dataset.openDevice, tab: "general" };
        this.render(false);
      });
    }
    this.shadowRoot.querySelector("[data-nav='back']")?.addEventListener("click", () => {
      this._screen = { name: "home", serial: null, tab: "general" };
      this.render(false);
    });
    for (const button of this.shadowRoot.querySelectorAll("[data-device-tab]")) {
      button.addEventListener("click", () => {
        this._screen = { name: "device", serial: button.dataset.serial, tab: button.dataset.deviceTab };
        this.render(false);
      });
    }
    for (const button of this.shadowRoot.querySelectorAll("[data-period]")) {
      button.addEventListener("click", () => {
        this._period[button.dataset.periodKind] = button.dataset.period;
        this.loadHistory(this._screen.serial, button.dataset.period);
        this.render(true);
      });
    }
    for (const button of this.shadowRoot.querySelectorAll("[data-action]")) {
      button.addEventListener("click", () => this.runAction(button.dataset.action));
    }
  }

  updateLive() {
    if (!this._hass || !this.shadowRoot) return;
    for (const device of this.devices()) {
      const online = this.isOnline(device);
      const voltage = numberState(this.metric(device, "voltage"))
        ?? numberState(this.metric(device, "last_voltage"));
      const stateNode = this.shadowRoot.querySelector(`[data-card-state="${CSS.escape(device.serial)}"]`);
      const voltageNode = this.shadowRoot.querySelector(`[data-card-voltage="${CSS.escape(device.serial)}"]`);
      const metaNode = this.shadowRoot.querySelector(`[data-card-meta="${CSS.escape(device.serial)}"]`);
      if (stateNode) stateNode.textContent = online ? this.t.powerOn : this.t.noContact;
      if (voltageNode) voltageNode.textContent = formatVoltage(voltage);
      if (metaNode) {
        // Same source as the first render, or the once-a-second tick would put
        // the Home Assistant restart time straight back.
        const uptimeSeconds = durationSeconds(this.metric(device, "uptime"));
        const elapsed = online && uptimeSeconds !== null
          ? duration(uptimeSeconds, this.language)
          : sinceIso(metaNode.dataset.statusMoment, this.language);
        metaNode.firstChild.textContent = `${online ? this.t.connectedFor : this.t.offlineFor} ${elapsed} `;
      }
    }

    if (this._screen.name !== "device") return;
    const device = this.device();
    if (!device) return;
    const online = this.isOnline(device);
    const power = this.shadowRoot.querySelector("[data-live-power]");
    const statusDuration = this.shadowRoot.querySelector("[data-live-duration]");
    if (power) power.textContent = online ? this.t.powerOn : this.t.noContact;
    if (statusDuration) statusDuration.textContent = this.statusDuration(device);

    const voltageNode = this.shadowRoot.querySelector("[data-live-voltage]");
    const voltageState = this.shadowRoot.querySelector("[data-live-voltage-state]");
    if (voltageNode) {
      const live = numberState(this.metric(device, "voltage"));
      const last = numberState(this.metric(device, "last_voltage"));
      voltageNode.textContent = formatVoltage(online ? live : last);
      if (voltageState) {
        const measuredAt = this.metric(device, "last_voltage")?.attributes?.measured_at;
        voltageState.textContent = online && live
          ? this.t.measuredNow
          : `${this.t.lastVoltageAt} ${measuredAt ? moment(Date.parse(measuredAt) / 1_000, this.language, true) : this.t.unavailable}`;
      }
    }
  }

  async runAction(action) {
    const device = this.device();
    if (!device) return;
    try {
      if (action === "phone-help") {
        this.showPhoneHelp();
        return;
      }
      if (action === "access-help") {
        this.showAccessHelp();
        return;
      }
      if (action === "rename-device") {
        const entity = this.metric(device, "display_name");
        const value = await this.promptText({
          title: this.t.renameDevice,
          description: this.t.renameHint,
          value: device.name,
          label: this.t.valueName,
          max: 40,
        });
        if (value === null) return;
        await this.callEntityService(entity, "text", "set_value", { value });
      } else if (action === "test-notification") {
        await this.callEntityService(
          this.metric(device, "test_notification"),
          "button",
          "press",
        );
      } else if (action === "set-voltage-min") {
        const entity = this.metric(device, "voltage_minimum");
        const current = numberState(entity) ?? 200;
        const value = await this.promptNumber({
          title: this.t.minimumLimit,
          description: this.language === "ro" ? "0 V dezactivează alerta. Valoarea recomandată inițial este 200 V." : "0 V disables the alert. The recommended initial value is 200 V.",
          value: current,
          min: 0,
          max: 260,
          step: 1,
          label: this.t.valueVolts,
        });
        if (value === null) return;
        await this.callEntityService(entity, "number", "set_value", { value });
      } else if (action === "set-notification-delay") {
        const entity = this.metric(device, "notification_delay");
        const current = numberState(entity) ?? 0;
        const value = await this.promptNumber({
          title: this.t.notificationDelay,
          description: this.t.notificationDelayHint,
          value: current,
          min: 0,
          max: 600,
          step: 1,
          label: this.t.valueSeconds,
        });
        if (value === null) return;
        await this.callEntityService(entity, "number", "set_value", { value });
      } else if (action === "calibrate") {
        const entity = this.metric(device, "calibration_reference");
        const value = await this.promptNumber({
          title: this.t.calibrateTitle,
          description: this.t.calibrateBody,
          value: 230,
          min: 50,
          max: 280,
          step: 0.1,
          label: this.t.valueVolts,
        });
        if (value === null) return;
        await this.callEntityService(entity, "number", "set_value", { value });
      } else if (action === "toggle-led") {
        const entity = this.metric(device, "idle_led");
        await this.callEntityService(entity, "switch", this.isOn(device, "idle_led") ? "turn_off" : "turn_on");
      } else if (action === "toggle-notifications") {
        const entity = this.metric(device, "automatic_notifications");
        await this.callEntityService(entity, "switch", this.isOn(device, "automatic_notifications") ? "turn_off" : "turn_on");
      } else if (action === "toggle-router-on-ups") {
        const entity = this.metric(device, "router_on_ups");
        await this.callEntityService(entity, "switch", this.isOn(device, "router_on_ups") ? "turn_off" : "turn_on");
      } else if (action === "toggle-diagnostic-logging") {
        const entity = this.metric(device, "diagnostic_logging");
        await this.callEntityService(entity, "switch", this.isOn(device, "diagnostic_logging") ? "turn_off" : "turn_on");
      } else if (action === "identify") {
        await this.callEntityService(this.metric(device, "identify"), "button", "press");
      } else if (action === "restart") {
        if (!await this.confirm(this.t.restartTitle, this.t.restartBody)) return;
        await this.callEntityService(this.metric(device, "restart"), "button", "press");
      } else if (action === "reset-calibration") {
        if (!await this.confirm(this.t.resetTitle, this.t.resetBody)) return;
        await this.callEntityService(this.metric(device, "reset_calibration"), "button", "press");
      } else if (action === "clear-history") {
        if (!await this.confirm(this.t.clearTitle, this.t.clearBody, true)) return;
        await this._hass.connection.sendMessagePromise({
          type: "aquanode_pulse/clear_history",
          serial: device.serial,
        });
        for (const period of PERIODS) this._history.delete(this.historyKey(device.serial, period));
        await this.loadHistory(device.serial, this._period.outage, true);
      }
      this.toast(this.t.done);
    } catch (error) {
      console.error("AquaNode Pulse action", action, error);
      this.toast(this.t.error, true);
    }
  }

  async callEntityService(entity, domain, service, data = {}) {
    if (!entity?.entity_id) throw new Error(this.t.notAvailable);
    await this._hass.callService(domain, service, {
      entity_id: entity.entity_id,
      ...data,
    });
  }

  promptNumber({ title, description, value, min, max, step, label }) {
    return new Promise((resolve) => {
      const root = this.shadowRoot.getElementById("modalRoot");
      root.innerHTML = `
        <div class="modal-backdrop">
          <form class="modal card">
            <span class="eyebrow">AQUANODE PULSE</span>
            <h2>${title}</h2>
            <p>${description}</p>
            <label>${label}<input type="number" value="${value}" min="${min}" max="${max}" step="${step}" required inputmode="decimal"></label>
            <div class="modal-actions">
              <button type="button" class="secondary-button cancel">${this.t.cancel}</button>
              <button type="submit" class="primary-button">${this.t.save}</button>
            </div>
          </form>
        </div>`;
      const finish = (result) => {
        root.replaceChildren();
        resolve(result);
      };
      root.querySelector(".cancel").addEventListener("click", () => finish(null));
      root.querySelector(".modal-backdrop").addEventListener("click", (event) => {
        if (event.target.classList.contains("modal-backdrop")) finish(null);
      });
      root.querySelector("form").addEventListener("submit", (event) => {
        event.preventDefault();
        const input = root.querySelector("input");
        const parsed = Number(input.value);
        if (!Number.isFinite(parsed) || parsed < min || parsed > max) return;
        finish(parsed);
      });
      requestAnimationFrame(() => root.querySelector("input").focus());
    });
  }

  promptText({ title, description, value, label, max }) {
    return new Promise((resolve) => {
      const root = this.shadowRoot.getElementById("modalRoot");
      root.innerHTML = `
        <div class="modal-backdrop">
          <form class="modal card">
            <span class="eyebrow">AQUANODE PULSE</span>
            <h2>${title}</h2>
            <p>${description}</p>
            <label>${label}<input type="text" value="${escapeHtml(value)}" maxlength="${max}" required autocomplete="off"></label>
            <div class="modal-actions">
              <button type="button" class="secondary-button cancel">${this.t.cancel}</button>
              <button type="submit" class="primary-button">${this.t.save}</button>
            </div>
          </form>
        </div>`;
      const finish = (result) => {
        root.replaceChildren();
        resolve(result);
      };
      root.querySelector(".cancel").addEventListener("click", () => finish(null));
      root.querySelector(".modal-backdrop").addEventListener("click", (event) => {
        if (event.target.classList.contains("modal-backdrop")) finish(null);
      });
      root.querySelector("form").addEventListener("submit", (event) => {
        event.preventDefault();
        const valueToSave = root.querySelector("input").value.trim();
        if (!valueToSave) return;
        finish(valueToSave);
      });
      requestAnimationFrame(() => {
        const input = root.querySelector("input");
        input.focus();
        input.select();
      });
    });
  }

  confirm(title, description, danger = false) {
    return new Promise((resolve) => {
      const root = this.shadowRoot.getElementById("modalRoot");
      root.innerHTML = `
        <div class="modal-backdrop">
          <div class="modal card">
            <span class="eyebrow">AQUANODE PULSE</span>
            <h2>${title}</h2>
            <p>${description}</p>
            <div class="modal-actions">
              <button class="secondary-button cancel">${this.t.cancel}</button>
              <button class="${danger ? "danger-button" : "primary-button"} confirm">${this.t.confirm}</button>
            </div>
          </div>
        </div>`;
      const finish = (result) => {
        root.replaceChildren();
        resolve(result);
      };
      root.querySelector(".cancel").addEventListener("click", () => finish(false));
      root.querySelector(".confirm").addEventListener("click", () => finish(true));
      root.querySelector(".modal-backdrop").addEventListener("click", (event) => {
        if (event.target.classList.contains("modal-backdrop")) finish(false);
      });
    });
  }

  showPhoneHelp() {
    const root = this.shadowRoot.getElementById("modalRoot");
    root.innerHTML = `
      <div class="modal-backdrop">
        <div class="modal help-modal card">
          <span class="eyebrow">HOME ASSISTANT</span>
          <h2>${this.t.phoneTitle}</h2>
          <p>${this.t.phoneIntro}</p>
          <ol>${this.t.phoneSteps.map((step) => `<li>${step}</li>`).join("")}</ol>
          <a class="primary-button import" href="${BLUEPRINT_IMPORT}" target="_blank" rel="noreferrer">${icon("phone")} ${this.t.importBlueprint}</a>
          <button class="secondary-button close">${this.t.close}</button>
        </div>
      </div>`;
    const close = () => root.replaceChildren();
    root.querySelector(".close").addEventListener("click", close);
    root.querySelector(".modal-backdrop").addEventListener("click", (event) => {
      if (event.target.classList.contains("modal-backdrop")) close();
    });
  }

  showAccessHelp() {
    const root = this.shadowRoot.getElementById("modalRoot");
    root.innerHTML = `
      <div class="modal-backdrop">
        <div class="modal help-modal card">
          <span class="eyebrow">HOME ASSISTANT</span>
          <h2>${this.t.accessTitle}</h2>
          <p>${this.t.accessBody}</p>
          <button class="secondary-button close">${this.t.close}</button>
        </div>
      </div>`;
    const close = () => root.replaceChildren();
    root.querySelector(".close").addEventListener("click", close);
    root.querySelector(".modal-backdrop").addEventListener("click", (event) => {
      if (event.target.classList.contains("modal-backdrop")) close();
    });
  }

  toast(message, error = false) {
    const node = this.shadowRoot.getElementById("toast");
    if (!node) return;
    node.textContent = message;
    node.className = `toast show ${error ? "error" : ""}`;
    window.clearTimeout(this._toastTimer);
    this._toastTimer = window.setTimeout(() => {
      node.className = "toast";
    }, 3_200);
  }

  get styles() {
    return `
      :host {
        --pulse-bg: #040b08;
        --pulse-bg-2: #07130d;
        --pulse-surface: rgba(13, 28, 20, .94);
        --pulse-surface-2: #12271b;
        --pulse-surface-3: #183322;
        --pulse-line: rgba(163, 206, 179, .14);
        --pulse-line-strong: rgba(163, 206, 179, .24);
        --pulse-text: #f1f7f3;
        --pulse-muted: #9eb3a6;
        --pulse-faint: #6f8979;
        --pulse-accent: #f7c95f;
        --pulse-ok: #58df8b;
        --pulse-warn: #f4bc4d;
        --pulse-bad: #ff7878;
        display: block;
        min-height: 100%;
        color: var(--pulse-text);
        background:
          radial-gradient(820px 480px at 85% -100px, rgba(72,176,107,.2), transparent 66%),
          radial-gradient(650px 430px at -10% 38%, rgba(247,201,95,.055), transparent 62%),
          linear-gradient(180deg, var(--pulse-bg-2), var(--pulse-bg) 48%);
        font: 16px/1.5 -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif;
        letter-spacing: -.006em;
        -webkit-font-smoothing: antialiased;
      }
      * { box-sizing: border-box; }
      button, input { font: inherit; }
      button { -webkit-tap-highlight-color: transparent; }
      .shell { min-height: 100vh; min-height: 100dvh; }
      .icon {
        width: 21px; height: 21px; display: block; fill: none; stroke: currentColor;
        stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round;
      }
      .icon.solid { fill: currentColor; stroke: none; }
      .topbar {
        position: sticky; z-index: 30; top: 0; min-height: 74px; display: flex;
        align-items: center; gap: 11px; padding: 10px max(18px, calc((100vw - 620px) / 2));
        border-bottom: 1px solid var(--pulse-line);
        background: color-mix(in srgb, var(--pulse-bg-2) 88%, transparent);
        backdrop-filter: blur(22px) saturate(150%);
      }
      .brand-mark {
        width: 40px; height: 40px; flex: none; display: grid; place-items: center;
        border: 1px solid rgba(247,201,95,.23); border-radius: 13px;
        color: var(--pulse-accent); background: rgba(247,201,95,.075);
      }
      .brand-mark .icon { width: 23px; height: 23px; }
      .titles { min-width: 0; flex: 1; }
      .brandline, .eyebrow {
        display: block; margin: 0 0 3px; color: var(--pulse-accent);
        font-size: 10px; font-weight: 760; letter-spacing: .14em; text-transform: uppercase;
      }
      .brandline b {
        margin-left: 5px; padding: 2px 5px; border: 1px solid rgba(88,223,139,.22);
        border-radius: 5px; color: var(--pulse-ok); font-size: 7px; letter-spacing: .1em;
      }
      .titles h1 { margin: 0; overflow: hidden; font-size: 17px; line-height: 1.2; text-overflow: ellipsis; white-space: nowrap; }
      .live-pill {
        display: flex; align-items: center; gap: 7px; padding: 7px 10px;
        border: 1px solid var(--pulse-line); border-radius: 999px; color: var(--pulse-muted);
        background: rgba(18,39,27,.8);
      }
      .live-pill span { width: 7px; height: 7px; border-radius: 50%; background: var(--pulse-ok); box-shadow: 0 0 0 4px rgba(88,223,139,.11); }
      .live-pill em { font-size: 9px; font-style: normal; font-weight: 720; letter-spacing: .08em; }
      .icon-button {
        width: 40px; height: 40px; display: grid; place-items: center; padding: 0;
        border: 1px solid var(--pulse-line); border-radius: 13px; color: var(--pulse-text);
        background: var(--pulse-surface); cursor: pointer;
      }
      main { width: min(620px, 100%); min-height: calc(100dvh - 74px); margin: 0 auto; padding: 16px 17px 18px; }
      /* Spacing used to come only from .section-head, so any two blocks that
         happened to follow each other without a heading between them sat flush:
         the voltage limit card and the incident journal touched. Excluding the
         heading on both sides keeps its own larger rhythm intact. */
      main > *:not(.section-head) + *:not(.section-head) { margin-top: 12px; }
      .card {
        position: relative; overflow: hidden; border: 1px solid var(--pulse-line);
        border-radius: 20px; background: linear-gradient(145deg, rgba(15,32,22,.98), var(--pulse-surface));
        box-shadow: 0 24px 70px -38px rgba(0,0,0,.96), 0 1px 0 rgba(255,255,255,.025) inset;
      }
      .home-hero {
        min-height: 154px; display: flex; justify-content: space-between; gap: 18px;
        padding: 25px 23px; overflow: hidden; border: 1px solid rgba(247,201,95,.24);
        border-radius: 28px; background: radial-gradient(230px 175px at 100% 0%, rgba(247,201,95,.22), transparent 70%), linear-gradient(140deg,#12271b,#0a1911 70%);
      }
      .home-hero.all-ok { border-color: rgba(88,223,139,.27); background: radial-gradient(230px 175px at 100% 0%,rgba(88,223,139,.19),transparent 70%),linear-gradient(140deg,#12291c,#091810 70%); }
      .home-hero > div:first-child { position: relative; z-index: 1; max-width: 350px; }
      .home-hero h2 { margin: 7px 0 8px; font-size: clamp(27px,7vw,36px); line-height: 1.04; letter-spacing: -.045em; }
      .home-hero p { margin: 0; color: var(--pulse-muted); font-size: 13.5px; }
      .hero-bolt {
        position: relative; z-index: 1; width: 64px; height: 64px; display: grid; place-items: center;
        flex: none; border: 1px solid rgba(247,201,95,.24); border-radius: 22px;
        color: var(--pulse-accent); background: rgba(247,201,95,.09); transform: rotate(4deg);
      }
      .hero-bolt .icon { width: 34px; height: 34px; }
      .section-head { margin: 27px 2px 11px; display: flex; align-items: end; justify-content: space-between; }
      .section-head h2 { margin: 0; font-size: 20px; line-height: 1.18; letter-spacing: -.025em; }
      .count { min-width: 28px; height: 28px; display: grid; place-items: center; border: 1px solid var(--pulse-line); border-radius: 10px; color: var(--pulse-muted); background: var(--pulse-surface); font-size: 12px; font-weight: 700; }
      .device-grid { display: grid; gap: 11px; }
      .device-card {
        width: 100%; min-height: 130px; display: grid; grid-template-columns: 48px 1fr auto;
        grid-template-rows: 1fr auto; gap: 12px 14px; padding: 17px; color: var(--pulse-text);
        text-align: left; cursor: pointer;
      }
      .rail { position: absolute; inset: 0 auto 0 0; width: 3px; background: var(--pulse-bad); box-shadow: 5px 0 28px rgba(255,120,120,.2); }
      .device-card.online .rail { background: var(--pulse-ok); box-shadow: 5px 0 28px rgba(88,223,139,.22); }
      .device-orb {
        width: 48px; height: 48px; display: grid; place-items: center; border: 1px solid var(--pulse-line);
        border-radius: 16px; color: var(--pulse-bad); background: var(--pulse-surface-2);
      }
      .device-card.online .device-orb { color: var(--pulse-ok); border-color: rgba(88,223,139,.24); background: rgba(88,223,139,.08); }
      .device-orb .icon { width: 25px; height: 25px; }
      .device-copy { min-width: 0; align-self: center; }
      .device-name { display: block; overflow: hidden; font-size: 17px; font-weight: 680; text-overflow: ellipsis; white-space: nowrap; }
      .device-state { margin-top: 6px; display: flex; align-items: center; gap: 7px; color: var(--pulse-bad); font-size: 13px; }
      .device-card.online .device-state { color: var(--pulse-ok); }
      .device-state i { width: 7px; height: 7px; border-radius: 50%; background: currentColor; box-shadow: 0 0 0 4px color-mix(in srgb,currentColor 11%,transparent); }
      .device-state b { font-weight: 600; }
      .device-side { display: flex; align-items: center; gap: 4px; color: var(--pulse-faint); }
      .device-side strong { color: var(--pulse-text); font-size: 14px; font-variant-numeric: tabular-nums; }
      .device-side .icon { width: 17px; }
      .device-foot { grid-column: 1/-1; padding-top: 11px; border-top: 1px solid var(--pulse-line); color: var(--pulse-faint); font-size: 11.5px; }
      .device-foot i { margin: 0 5px; opacity: .5; }
      .empty { padding: 34px 24px; text-align: center; }
      .empty-icon { width: 58px; height: 58px; margin: 0 auto 16px; display: grid; place-items: center; border-radius: 19px; color: var(--pulse-accent); background: rgba(247,201,95,.08); }
      .empty h3 { margin: 0 0 6px; }
      .empty p { margin: 0; color: var(--pulse-muted); }
      .local-note { margin: 20px 3px; display: flex; align-items: flex-start; gap: 11px; color: var(--pulse-muted); }
      .local-note > .icon { width: 18px; flex: none; margin-top: 1px; color: var(--pulse-ok); }
      .local-note strong, .local-note span { display: block; font-size: 12px; }
      .local-note span { margin-top: 2px; color: var(--pulse-faint); }
      .status-hero {
        min-height: 292px; padding: 28px 20px 25px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; text-align: center; border-radius: 28px;
        background: radial-gradient(250px 185px at 50% 15%,rgba(88,223,139,.12),transparent 72%),linear-gradient(165deg,var(--pulse-surface-2),var(--pulse-surface));
      }
      .status-hero.bad { background: radial-gradient(250px 185px at 50% 15%,rgba(255,120,120,.12),transparent 72%),linear-gradient(165deg,var(--pulse-surface-2),var(--pulse-surface)); }
      .status-ring {
        width: 92px; height: 92px; margin: 16px 0 18px; display: grid; place-items: center;
        border: 1px solid rgba(88,223,139,.3); border-radius: 31px; color: var(--pulse-ok);
        background: rgba(88,223,139,.08); transform: rotate(5deg);
      }
      .status-hero.bad .status-ring { color: var(--pulse-bad); border-color: rgba(255,120,120,.28); background: rgba(255,120,120,.08); }
      .status-ring .icon { width: 44px; height: 44px; transform: rotate(-5deg); }
      .status-hero h2 { margin: 0 0 4px; font-size: 26px; letter-spacing: -.035em; }
      .status-hero > strong { color: var(--pulse-ok); font-size: 15px; }
      .status-hero.bad > strong { color: var(--pulse-bad); }
      .status-hero p { margin: 6px 0 0; color: var(--pulse-faint); font-size: 12.5px; }
      .status-hero small { margin-top: 8px; color: var(--pulse-muted); }
      .chart-card { padding: 14px; }
      .period-tabs { display: flex; gap: 3px; padding: 3px; border: 1px solid var(--pulse-line); border-radius: 12px; background: rgba(18,39,27,.82); }
      .period-tabs button { min-height: 34px; flex: 1; padding: 7px 8px; border: 0; border-radius: 9px; color: var(--pulse-faint); background: transparent; font-size: 11.5px; font-weight: 700; cursor: pointer; }
      .period-tabs button.on { color: var(--pulse-accent); background: rgba(247,201,95,.1); }
      .chart-copy { margin: 17px 4px 6px; }
      .chart-copy strong, .chart-copy span { display: block; }
      .chart-copy strong { font-size: 14px; }
      .chart-copy span, .chart-note { margin-top: 3px; color: var(--pulse-faint); font-size: 10.5px; }
      .outage-chart, .voltage-chart { width: 100%; height: auto; display: block; overflow: visible; }
      .outage-chart line, .grid-lines line { stroke: var(--pulse-line-strong); stroke-width: 1; }
      .outage-chart rect { fill: rgba(111,137,121,.22); }
      .outage-chart rect.has-value { fill: var(--pulse-accent); }
      .outage-chart text, .voltage-chart text { fill: var(--pulse-faint); font-size: 8px; text-anchor: middle; }
      .chart-empty { min-height: 150px; display: grid; place-items: center; color: var(--pulse-faint); font-size: 13px; }
      .event-row { overflow: hidden; border: 1px solid var(--pulse-line); border-radius: 14px; background: var(--pulse-surface-2); }
      .event-row + .event-row { margin-top: 8px; }
      .event-row summary { min-height: 62px; display: flex; align-items: center; gap: 11px; padding: 11px 13px; list-style: none; cursor: pointer; }
      .event-row summary::-webkit-details-marker { display: none; }
      .event-dot { width: 9px; height: 9px; flex: none; border-radius: 50%; background: var(--pulse-faint); box-shadow: 0 0 0 4px rgba(111,137,121,.09); }
      .event-row.power .event-dot { background: var(--pulse-bad); box-shadow: 0 0 0 4px rgba(255,120,120,.09); }
      .event-row.voltage .event-dot { background: var(--pulse-warn); box-shadow: 0 0 0 4px rgba(244,188,77,.09); }
      .event-row.maintenance .event-dot { background: #75a7ff; box-shadow: 0 0 0 4px rgba(117,167,255,.09); }
      .event-copy { min-width: 0; flex: 1; }
      .event-copy strong, .event-copy small { display: block; }
      .event-copy strong { font-size: 13.5px; }
      .event-copy small { margin-top: 2px; color: var(--pulse-faint); font-size: 11.5px; }
      .event-row summary > .icon { width: 17px; color: var(--pulse-faint); transition: transform .2s ease; }
      .event-row[open] summary > .icon { transform: rotate(90deg); }
      .event-row dl { margin: 0; padding: 13px; border-top: 1px solid var(--pulse-line); background: rgba(24,51,34,.4); }
      .event-row dl div { display: flex; justify-content: space-between; gap: 12px; padding: 3px 0; font-size: 12px; }
      .event-row dt { color: var(--pulse-faint); }
      .event-row dd { margin: 0; color: var(--pulse-text); }
      .empty-row { padding: 20px; color: var(--pulse-muted); font-size: 13px; }
      .journal-actions { margin-top: 10px; display: flex; align-items: center; justify-content: space-between; gap: 12px; }
      .journal-actions > span { display: flex; align-items: center; gap: 6px; color: var(--pulse-faint); font-size: 10.5px; }
      .journal-actions > span .icon { width: 15px; color: var(--pulse-ok); }
      .text-button { display: flex; align-items: center; gap: 7px; padding: 8px; border: 0; color: var(--pulse-muted); background: none; font-size: 11px; cursor: pointer; }
      .text-button .icon { width: 16px; }
      .text-button.danger { color: var(--pulse-bad); }
      .voltage-hero {
        min-height: 248px; display: flex; flex-direction: column; align-items: center;
        justify-content: center; padding: 27px 20px; border-radius: 28px; text-align: center;
        background: radial-gradient(270px 190px at 50% 25%,rgba(247,201,95,.12),transparent 72%),linear-gradient(165deg,var(--pulse-surface-2),var(--pulse-surface));
      }
      .voltage-hero.ok { border-color: rgba(88,223,139,.23); background: radial-gradient(270px 190px at 50% 25%,rgba(88,223,139,.13),transparent 72%),linear-gradient(165deg,var(--pulse-surface-2),var(--pulse-surface)); }
      .voltage-hero.warning { border-color: rgba(244,188,77,.43); }
      .voltage-hero > strong { margin: 14px 0 8px; color: var(--pulse-text); font-size: clamp(54px,16vw,78px); line-height: 1; letter-spacing: -.065em; font-variant-numeric: tabular-nums; }
      .voltage-hero.ok > strong { color: var(--pulse-ok); }
      .voltage-hero.warning > strong { color: var(--pulse-warn); }
      .voltage-hero p { margin: 0; color: var(--pulse-muted); font-size: 12.5px; }
      .warning-pill { margin-top: 14px; padding: 7px 10px; border: 1px solid rgba(244,188,77,.25); border-radius: 10px; color: var(--pulse-warn); background: rgba(244,188,77,.07); font-size: 11.5px; font-weight: 650; }
      .voltage-summary { display: grid; grid-template-columns: repeat(3,1fr); gap: 7px; margin: 15px 1px 2px; }
      .voltage-summary span { padding: 9px; border: 1px solid var(--pulse-line); border-radius: 11px; background: rgba(18,39,27,.6); text-align: center; }
      .voltage-summary small, .voltage-summary strong { display: block; }
      .voltage-summary small { color: var(--pulse-faint); font-size: 9px; text-transform: uppercase; letter-spacing: .08em; }
      .voltage-summary strong { margin-top: 2px; color: var(--pulse-text); font-size: 13px; }
      .voltage-band { fill: rgba(88,223,139,.1); stroke: none; }
      .voltage-line { fill: none; stroke: var(--pulse-ok); stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; }
      .threshold { stroke: var(--pulse-warn); stroke-width: 1.2; stroke-dasharray: 4 4; opacity: .8; }
      .voltage-chart .grid-lines text { text-anchor: end; }
      .voltage-chart .time.start { text-anchor: start; }
      .voltage-chart .time.end { text-anchor: end; }
      .chart-note { margin: 4px 4px 2px; }
      .limit-card { padding: 18px; }
      .limit-card > div { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
      .limit-card > div span { color: var(--pulse-muted); font-size: 13px; }
      .limit-card > div strong { color: var(--pulse-accent); font-size: 21px; }
      .limit-card p { margin: 8px 0 14px; color: var(--pulse-muted); font-size: 13px; }
      .settings-rows { padding: 0; }
      .settings-row {
        width: 100%; min-height: 68px; display: flex; align-items: center; gap: 12px; padding: 12px 15px;
        border: 0; color: var(--pulse-text); background: transparent; text-align: left; cursor: pointer;
      }
      .settings-row + .settings-row { border-top: 1px solid var(--pulse-line); }
      .settings-row:active { background: var(--pulse-surface-2); }
      .row-icon { width: 36px; height: 36px; flex: none; display: grid; place-items: center; border-radius: 11px; color: var(--pulse-muted); background: var(--pulse-surface-2); }
      .row-icon .icon { width: 18px; height: 18px; }
      .row-copy { min-width: 0; flex: 1; }
      .row-copy strong, .row-copy small { display: block; }
      .row-copy strong { font-size: 14px; font-weight: 650; }
      .row-copy small { margin-top: 2px; color: var(--pulse-faint); font-size: 10.5px; line-height: 1.35; }
      .row-value { max-width: 110px; color: var(--pulse-muted); font-size: 11.5px; text-align: right; }
      .settings-row > .icon { width: 16px; color: var(--pulse-faint); }
      .settings-row.danger { color: var(--pulse-bad); }
      .toggle { width: 42px; height: 24px; flex: none; padding: 3px; border-radius: 99px; background: var(--pulse-surface-3); transition: background .2s; }
      .toggle i { width: 18px; height: 18px; display: block; border-radius: 50%; background: var(--pulse-muted); transition: transform .2s,background .2s; }
      .toggle.on { background: rgba(88,223,139,.25); }
      .toggle.on i { background: var(--pulse-ok); transform: translateX(18px); }
      .diagnostics { margin-top: 28px; padding: 0; }
      .diagnostics summary { min-height: 72px; display: flex; align-items: center; justify-content: space-between; padding: 15px 18px; list-style: none; cursor: pointer; }
      .diagnostics summary::-webkit-details-marker { display: none; }
      .diagnostics summary strong { display: block; font-size: 17px; }
      .diagnostics summary > .icon { color: var(--pulse-faint); transition: transform .2s; }
      .diagnostics[open] summary > .icon { transform: rotate(90deg); }
      .diagnostic-list { border-top: 1px solid var(--pulse-line); }
      .info-row { min-height: 55px; display: grid; grid-template-columns: 36px 1fr auto; align-items: center; gap: 11px; padding: 9px 15px; }
      .info-row + .info-row { border-top: 1px solid var(--pulse-line); }
      .info-row > span:not(.row-icon) { color: var(--pulse-muted); font-size: 12.5px; }
      .info-row > strong { max-width: 190px; overflow-wrap: anywhere; font-size: 12px; text-align: right; }
      .device-tabs {
        position: sticky; z-index: 42; bottom: max(8px,env(safe-area-inset-bottom));
        width: min(calc(100% - 24px),460px); margin: 0 auto; display: flex; gap: 5px; padding: 6px;
        border: 1px solid var(--pulse-line-strong); border-radius: 22px;
        background: rgba(13,28,20,.94); box-shadow: 0 18px 52px -18px rgba(0,0,0,.82);
        backdrop-filter: blur(24px) saturate(160%);
      }
      .device-tabs button { min-height: 49px; flex: 1; display: flex; align-items: center; justify-content: center; gap: 7px; padding: 7px 8px; border: 0; border-radius: 16px; color: var(--pulse-faint); background: transparent; font-size: 11.5px; font-weight: 680; cursor: pointer; }
      .device-tabs button.on { color: var(--pulse-accent); background: rgba(247,201,95,.1); }
      .device-tabs .icon { width: 19px; }
      .secondary-button, .primary-button, .danger-button {
        min-height: 42px; display: inline-flex; align-items: center; justify-content: center; gap: 8px;
        padding: 9px 15px; border: 1px solid var(--pulse-line); border-radius: 12px;
        color: var(--pulse-text); background: var(--pulse-surface-2); font-weight: 650; text-decoration: none; cursor: pointer;
      }
      .primary-button { border-color: rgba(247,201,95,.35); color: #241900; background: var(--pulse-accent); }
      .danger-button { border-color: rgba(255,120,120,.35); color: #270606; background: var(--pulse-bad); }
      .modal-backdrop { position: fixed; z-index: 100; inset: 0; display: grid; place-items: center; padding: 18px; background: rgba(0,0,0,.68); backdrop-filter: blur(8px); }
      .modal { width: min(440px,100%); padding: 22px; overflow: visible; }
      .modal h2 { margin: 6px 0 7px; font-size: 23px; letter-spacing: -.03em; }
      .modal p { margin: 0 0 18px; color: var(--pulse-muted); font-size: 13px; }
      .modal label { display: grid; gap: 7px; color: var(--pulse-muted); font-size: 12px; }
      .modal input { width: 100%; padding: 13px 14px; border: 1px solid var(--pulse-line-strong); border-radius: 12px; outline: 0; color: var(--pulse-text); background: var(--pulse-bg); font-size: 17px; }
      .modal input:focus { border-color: var(--pulse-accent); box-shadow: 0 0 0 3px rgba(247,201,95,.08); }
      .modal-actions { margin-top: 19px; display: flex; justify-content: flex-end; gap: 8px; }
      .help-modal ol { margin: 0 0 18px; padding-left: 21px; color: var(--pulse-muted); }
      .help-modal li { margin: 8px 0; padding-left: 4px; font-size: 13px; }
      .help-modal .import { width: 100%; }
      .help-modal .close { width: 100%; margin-top: 8px; }
      .toast {
        position: fixed; z-index: 120; left: 50%; bottom: 86px; max-width: calc(100% - 32px);
        padding: 11px 15px; border: 1px solid rgba(88,223,139,.3); border-radius: 12px;
        color: var(--pulse-text); background: rgba(13,28,20,.97); box-shadow: 0 16px 44px rgba(0,0,0,.45);
        opacity: 0; pointer-events: none; transform: translate(-50%,12px); transition: opacity .2s,transform .2s;
        font-size: 12.5px; text-align: center;
      }
      .toast.show { opacity: 1; transform: translate(-50%,0); }
      .toast.error { border-color: rgba(255,120,120,.35); }
      .loading { padding: 40px; color: var(--pulse-muted); }
      @media (max-width: 480px) {
        .live-pill em { display: none; }
        .live-pill { padding: 9px; }
        .device-side strong { display: none; }
        .home-hero { min-height: 145px; padding: 22px 20px; }
        .hero-bolt { width: 56px; height: 56px; border-radius: 19px; }
        .journal-actions { align-items: flex-start; flex-direction: column; }
        .row-value { max-width: 82px; }
      }
      @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { scroll-behavior: auto !important; transition: none !important; }
      }
    `;
  }
}

if (!customElements.get("aquanode-pulse-panel")) {
  customElements.define("aquanode-pulse-panel", AquaNodePulsePanel);
}
