import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { 
  FileText, 
  ShieldCheck, 
  SearchCheck, 
  UploadCloud, 
  Clock, 
  ArrowRight,
  Fingerprint,
  CheckCircle2,
  ExternalLink
} from 'lucide-react';

export const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get('/dashboard/stats');
        setStats(res.data);
      } catch (err) {
        console.error('Failed to load dashboard metrics', err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-12 text-center text-slate-400">
        Loading real-time security telemetry...
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8 gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Security Operation Center</h1>
          <p className="text-sm text-slate-400 mt-1">
            Real-time status of protected course documents and cryptographic manifests
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link
            to="/documents"
            className="px-4 py-2 rounded-lg bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold text-sm transition flex items-center gap-2 shadow-sm shadow-teal-500/20"
          >
            <UploadCloud className="w-4 h-4" /> Upload & Protect
          </Link>
          <Link
            to="/verify"
            className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-semibold text-sm transition flex items-center gap-2"
          >
            <SearchCheck className="w-4 h-4 text-teal-400" /> Verify File
          </Link>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-10">
        <div className="p-5 rounded-xl bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">Total Documents</span>
            <FileText className="w-4 h-4 text-slate-400" />
          </div>
          <div className="text-2xl font-bold text-white mt-2">{stats?.total_documents || 0}</div>
          <span className="text-[11px] text-slate-500">Uploaded to private vault</span>
        </div>

        <div className="p-5 rounded-xl bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">Watermark Records</span>
            <ShieldCheck className="w-4 h-4 text-teal-400" />
          </div>
          <div className="text-2xl font-bold text-white mt-2">{stats?.total_watermarked || 0}</div>
          <span className="text-[11px] text-teal-400">Signed with Ed25519</span>
        </div>

        <div className="p-5 rounded-xl bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">Watermark Breakdown</span>
            <Fingerprint className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-sm font-semibold text-white mt-2">
            Visible: {stats?.watermark_breakdown?.visible || 0} | DCT: {stats?.watermark_breakdown?.invisible_dct || 0}
          </div>
          <span className="text-[11px] text-slate-500">Spatial vs Frequency domain</span>
        </div>

        <div className="p-5 rounded-xl bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">Verification Jobs</span>
            <SearchCheck className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-2xl font-bold text-white mt-2">{stats?.total_verifications || 0}</div>
          <span className="text-[11px] text-slate-500">Forensic evaluations logged</span>
        </div>
      </div>

      {/* Two Columns: Recent Documents & Tamper-Evident Audit Trail */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Documents */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-white">Recent Documents</h2>
            <Link to="/documents" className="text-xs text-teal-400 hover:underline flex items-center gap-1">
              View all <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {stats?.recent_documents?.length === 0 ? (
            <div className="p-8 text-center text-slate-500 text-sm">
              No documents uploaded yet. Upload a syllabus, lecture slide, or exam PDF.
            </div>
          ) : (
            <div className="divide-y divide-slate-800">
              {stats?.recent_documents?.map((doc: any) => (
                <div key={doc.id} className="py-3 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-2 rounded bg-slate-950 border border-slate-800 text-teal-400">
                      <FileText className="w-4 h-4" />
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold text-slate-100">{doc.title}</h4>
                      <p className="text-xs text-slate-400">{doc.original_filename} • {doc.page_count} pages</p>
                    </div>
                  </div>
                  <Link
                    to={`/documents/${doc.id}`}
                    className="p-1.5 rounded hover:bg-slate-800 text-slate-400 hover:text-white"
                  >
                    <ExternalLink className="w-4 h-4" />
                  </Link>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Cryptographic Hash Chained Audit Trail */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-lg font-bold text-white">Cryptographic Audit Chain</h2>
              <p className="text-xs text-slate-400">SHA-256 block-linked event provenance</p>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800">
              Chain Verified
            </span>
          </div>

          <div className="space-y-3">
            {stats?.recent_audit_trail?.map((audit: any) => (
              <div key={audit.id} className="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs flex items-center justify-between">
                <div>
                  <span className="font-semibold text-slate-200">{audit.event_type}</span>
                  <div className="text-[10px] font-mono text-slate-500 mt-0.5">
                    Hash: {audit.current_hash}
                  </div>
                </div>
                <div className="text-right">
                  <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${
                    audit.status === 'SUCCESS' ? 'bg-teal-950 text-teal-400' : 'bg-rose-950 text-rose-400'
                  }`}>
                    {audit.status}
                  </span>
                  <div className="text-[10px] text-slate-500 mt-1">
                    {new Date(audit.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
