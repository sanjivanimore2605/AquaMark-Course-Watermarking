import React, { useState } from 'react';
import api from '../services/api';
import { 
  FileCheck2, 
  UploadCloud, 
  ShieldCheck, 
  ShieldAlert, 
  FileText, 
  CheckCircle2, 
  XCircle,
  Download,
  AlertTriangle
} from 'lucide-react';

export const Verify: React.FC = () => {
  const [candidateFile, setCandidateFile] = useState<File | null>(null);
  const [manifestFile, setManifestFile] = useState<File | null>(null);
  const [verifying, setVerifying] = useState(false);
  const [result, setResult] = useState<any | null>(null);
  const [error, setError] = useState('');

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!candidateFile) {
      setError('Please select a candidate PDF to verify.');
      return;
    }

    setVerifying(true);
    setError('');
    setResult(null);

    const formData = new FormData();
    formData.append('file', candidateFile);
    if (manifestFile) {
      formData.append('manifest_file', manifestFile);
    }

    try {
      const res = await api.post('/verify', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Verification request failed.');
    } finally {
      setVerifying(false);
    }
  };

  const getVerdictBadge = (verdict: string) => {
    if (verdict === 'AUTHENTIC_EXACT_MATCH') {
      return (
        <div className="flex items-center gap-2 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
          <CheckCircle2 className="w-5 h-5 shrink-0" />
          <div>
            <div className="font-bold text-sm">Authentic: Exact Bit-Level Match</div>
            <div className="text-xs text-emerald-300">File is 100% identical to the recorded protected PDF. Signature and manifest valid.</div>
          </div>
        </div>
      );
    } else if (verdict === 'AUTHENTIC_WATERMARK_CONFIRMED') {
      return (
        <div className="flex items-center gap-2 p-3 rounded-xl bg-teal-500/10 border border-teal-500/30 text-teal-400">
          <ShieldCheck className="w-5 h-5 shrink-0" />
          <div>
            <div className="font-bold text-sm">Authentic: Watermark Forensic Confirmed</div>
            <div className="text-xs text-teal-300">File has undergone transformation, but embedded DCT watermark payload was successfully extracted.</div>
          </div>
        </div>
      );
    } else if (verdict === 'TAMPERED_DOCUMENT_MODIFIED') {
      return (
        <div className="flex items-center gap-2 p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400">
          <XCircle className="w-5 h-5 shrink-0" />
          <div>
            <div className="font-bold text-sm">Tampering Detected</div>
            <div className="text-xs text-rose-300">The file hash does not match the manifest record, indicating unauthorized document modification.</div>
          </div>
        </div>
      );
    } else {
      return (
        <div className="flex items-center gap-2 p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-400">
          <AlertTriangle className="w-5 h-5 shrink-0" />
          <div>
            <div className="font-bold text-sm">Unregistered or Unverified Document</div>
            <div className="text-xs text-amber-300">No cryptographic record or valid signature found in the authority vault.</div>
          </div>
        </div>
      );
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="text-center mb-10">
        <div className="inline-flex p-3 bg-teal-500/10 rounded-2xl text-teal-400 mb-3 border border-teal-500/20">
          <FileCheck2 className="w-8 h-8" />
        </div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">Cryptographic Verification Center</h1>
        <p className="text-sm text-slate-400 mt-2 max-w-xl mx-auto">
          Verify digital authenticity, check for unauthorized alterations, evaluate Ed25519 signatures, and extract embedded steganographic watermarks.
        </p>
      </div>

      {error && (
        <div className="p-4 mb-6 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
          {error}
        </div>
      )}

      {/* Verification Form */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-xl mb-8">
        <form onSubmit={handleVerify} className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-slate-200 mb-2">Candidate Document (PDF)</label>
            <div className="border-2 border-dashed border-slate-700 hover:border-teal-500/50 rounded-xl p-6 text-center cursor-pointer bg-slate-950/40 transition">
              <input
                type="file"
                accept=".pdf"
                required
                onChange={(e) => setCandidateFile(e.target.files?.[0] || null)}
                className="hidden"
                id="cand-pdf"
              />
              <label htmlFor="cand-pdf" className="cursor-pointer">
                <UploadCloud className="w-8 h-8 text-slate-400 mx-auto mb-2" />
                <span className="text-sm font-semibold text-teal-400">
                  {candidateFile ? candidateFile.name : 'Choose Candidate PDF to Inspect'}
                </span>
                <p className="text-xs text-slate-500 mt-1">Upload the document suspected of being modified or leaked</p>
              </label>
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-200 mb-2">
              Cryptographic Manifest JSON <span className="text-slate-500 font-normal">(Optional for detached verification)</span>
            </label>
            <div className="border border-slate-800 rounded-xl p-4 bg-slate-950/40">
              <input
                type="file"
                accept=".json"
                onChange={(e) => setManifestFile(e.target.files?.[0] || null)}
                className="text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-slate-800 file:text-slate-200 hover:file:bg-slate-700"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={verifying}
            className="w-full py-3 rounded-xl bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold transition flex items-center justify-center gap-2 text-sm shadow-md shadow-teal-500/20 disabled:opacity-50"
          >
            {verifying ? 'Evaluating Signatures & Forensics...' : 'Run Forensic Evaluation'}
          </button>
        </form>
      </div>

      {/* Verification Results Panel */}
      {result && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-xl">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-bold text-white">Forensic Analysis Report</h3>
            <a
              href={`/api/v1/verify/reports/${result.id}/pdf`}
              className="px-3 py-1.5 rounded-lg bg-teal-500/10 hover:bg-teal-500/20 text-teal-300 border border-teal-500/30 text-xs font-semibold transition flex items-center gap-1.5"
            >
              <Download className="w-3.5 h-3.5" /> Download Official Certificate (PDF)
            </a>
          </div>

          <div className="mb-6">
            {getVerdictBadge(result.status_summary)}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
              <div className="font-semibold text-slate-400 mb-1">Candidate File SHA-256</div>
              <div className="font-mono text-slate-200 break-all">{result.candidate_sha256}</div>
            </div>

            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
              <div className="font-semibold text-slate-400 mb-1">Ed25519 Digital Signature</div>
              <div className="text-slate-200 font-semibold">
                {result.signature_valid ? 'VALID (Matches Root Authority Key)' : 'INVALID / MISSING'}
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
              <div className="font-semibold text-slate-400 mb-1">Digital Watermark Detection</div>
              <div className="text-slate-200 font-semibold">
                {result.watermark_detected ? `DETECTED (${result.full_report?.watermark_algorithm || 'DCT'})` : 'NOT DETECTED'}
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
              <div className="font-semibold text-slate-400 mb-1">Extracted Payload / Identity</div>
              <div className="text-teal-400 font-mono font-bold">
                {result.extracted_payload || 'None extracted'}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
