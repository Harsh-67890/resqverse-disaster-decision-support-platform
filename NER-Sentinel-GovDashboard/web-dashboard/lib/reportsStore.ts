export interface IncidentReportItem {
  report_id: string;
  device_id: string;
  lat: number;
  lng: number;
  report_type: string;
  timestamp: number;
  offline_synced: boolean;
  image_url?: string;
}

// Global in-memory store preserved across serverless hot reloads in globalThis
const globalStore = globalThis as unknown as {
  __ner_reports_store?: IncidentReportItem[];
};

if (!globalStore.__ner_reports_store) {
  globalStore.__ner_reports_store = [
    {
      report_id: "RPT-1001",
      device_id: "phone_001_NER_SDRF",
      lat: 27.2789,
      lng: 88.5944,
      report_type: "FLOOD",
      timestamp: Date.now() - 360000,
      offline_synced: true,
    },
    {
      report_id: "RPT-1002",
      device_id: "phone_002_FIELD_AGENT",
      lat: 27.3150,
      lng: 88.6190,
      report_type: "LANDSLIDE",
      timestamp: Date.now() - 180000,
      offline_synced: true,
    },
    {
      report_id: "RPT-1003",
      device_id: "phone_003_CITIZEN",
      lat: 27.3389,
      lng: 88.6065,
      report_type: "ROAD_DAMAGE",
      timestamp: Date.now() - 60000,
      offline_synced: true,
    }
  ];
}

export function getReports(): IncidentReportItem[] {
  return globalStore.__ner_reports_store || [];
}

export function addReport(report: IncidentReportItem): IncidentReportItem {
  if (!globalStore.__ner_reports_store) {
    globalStore.__ner_reports_store = [];
  }
  globalStore.__ner_reports_store.push(report);
  return report;
}
