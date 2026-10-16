import { NextRequest, NextResponse } from "next/server";
import { getReports, addReport, IncidentReportItem } from "@/lib/reportsStore";

export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData();
    const reports = getReports();
    const report_id = `RPT-${reports.length + 1001}`;

    const device_id = (formData.get("device_id") as string) || "phone_001";
    const lat = Number(formData.get("lat")) || 27.3389;
    const lng = Number(formData.get("lng")) || 88.6065;
    const report_type = ((formData.get("report_type") as string) || "FLOOD").toUpperCase();
    const timestamp = Number(formData.get("timestamp")) || Date.now();

    const newReport: IncidentReportItem = {
      report_id,
      device_id,
      lat,
      lng,
      report_type,
      timestamp,
      offline_synced: true,
      image_url: "/ai-bot-avatar.png",
    };

    addReport(newReport);

    return NextResponse.json({
      success: true,
      status: "SUCCESS",
      report_id,
      zone_id: "ZONE-A",
      sync_status: "synced",
      image_url: "/ai-bot-avatar.png",
      message: "Incident report with image registered successfully.",
      report: newReport,
      total_reports: reports.length,
    });
  } catch (err: any) {
    return NextResponse.json(
      { success: false, error: err.message || "Failed to process multipart report" },
      { status: 400 }
    );
  }
}
