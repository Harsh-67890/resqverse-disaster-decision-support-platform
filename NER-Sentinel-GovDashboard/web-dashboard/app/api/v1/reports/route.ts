import { NextRequest, NextResponse } from "next/server";
import { getReports, addReport, IncidentReportItem } from "@/lib/reportsStore";

export async function GET() {
  const reports = getReports();
  return NextResponse.json({
    success: true,
    total: reports.length,
    reports: [...reports].reverse(),
    latest: reports[reports.length - 1] || null,
  });
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const reports = getReports();
    const report_id = `RPT-${reports.length + 1001}`;

    const newReport: IncidentReportItem = {
      report_id,
      device_id: body.device_id || body.deviceId || "phone_001",
      lat: Number(body.lat) || 27.3389,
      lng: Number(body.lng) || 88.6065,
      report_type: (body.report_type || body.reportType || "FLOOD").toUpperCase(),
      timestamp: body.timestamp || Date.now(),
      offline_synced: true,
    };

    addReport(newReport);

    return NextResponse.json({
      success: true,
      status: "SUCCESS",
      report_id,
      zone_id: "ZONE-A",
      sync_status: "synced",
      message: "Incident report registered in NER-Sentinel engine.",
      report: newReport,
      total_reports: reports.length,
    });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message || "Failed to process report" },
      { status: 400 }
    );
  }
}
