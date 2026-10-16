import { NextResponse } from "next/server";
import { getReports } from "@/lib/reportsStore";

export async function GET() {
  const reports = getReports();
  const latest = reports.length > 0 ? reports[reports.length - 1] : null;
  return NextResponse.json({
    success: true,
    latest,
  });
}
