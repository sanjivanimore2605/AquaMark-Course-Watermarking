import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { 
  FileText, 
  UploadCloud, 
  ShieldCheck, 
  Search, 
  Download, 
  Layers, 
  AlertCircle,
  Plus,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  ExternalLink,
  FileCheck
} from 'lucide-react';

export const Documents: React.FC = () => {
  const [docs, setDocs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState('');
  const [search, setSearch] = useState('');
  const [expandedDocIds, setExpandedDocIds] = useState<Record<string, boolean>>({});

  // Watermark modal state
  const [selectedDoc, setSelectedDoc] = useState<any | null>(null);
  const [wmType, setWmType] = useState('visible');
  const [wmText, setWmText] = useState('CONFIDENTIAL - CS401');
  const [recipientId, setRecipientId] = useState('');
  const [applyingWm, setApplyingWm] = useState(false);
  const [wmSuccess, setWmSuccess] = useState<any | null>(null);

  const toggleExpand = (docId: string) => {
    setExpandedDocIds(prev => ({ ...prev, [docId]: !prev[docId] }));
  };

  const handleDownloadFile = async (url: string, filename: string) => {
    try {
      const res = await api.get(url, { responseType: 'blob' });
      const contentType = String(res.headers['content-type'] || 'application/pdf');
      const blobUrl = window.URL.createObjectURL(new Blob([res.data], { type: contentType }));
      const a = document.createElement('a');
      a.href = blobUrl;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(blobUrl);
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to download file.');
    }
  };

  const handleViewPdf = async (url: string) => {
    try {
      const res = await api.get(url, { responseType: 'blob' });
      const blobUrl = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }));
      window.open(blobUrl, '_blank');
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to open PDF in new tab.');
    }
  };

  const fetchDocs = async () => {
    try {
      const res = await api.get('/documents');
      setDocs(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocs();
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setUploadError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      await api.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      fetchDocs();
    } catch (err: any) {
      setUploadError(err.response?.data?.detail || 'Failed to upload PDF.');
    } finally {
      setUploading(false);
    }
  };

  const handleApplyWatermark = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedDoc) return;

    setApplyingWm(true);
    setWmSuccess('');

    try {
      const res = await api.post('/watermarks/apply', {
        document_id: selectedDoc.id,
        watermark_type: wmType,
        text: wmText,
        recipient_identifier: recipientId || undefined,
        opacity: 0.35,
        font_size: 38.0
      });

      setWmSuccess(res.data);
      setExpandedDocIds(prev => ({ ...prev, [selectedDoc.id]: true }));
      fetchDocs();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Watermark failed to apply.');
    } finally {
      setApplyingWm(false);
    }
  };

  const filteredDocs = docs.filter(d => 
    d.title.toLowerCase().includes(search.toLowerCase()) || 
    d.original_filename.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Course Documents</h1>
          <p className="text-sm text-slate-400 mt-1">Manage, watermark, and generate cryptographic manifests for PDF assets</p>
        </div>

        <div className="flex items-center gap-3">
          <label className="cursor-pointer px-4 py-2 rounded-lg bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold text-sm transition flex items-center gap-2 shadow-sm shadow-teal-500/20">
            <UploadCloud className="w-4 h-4" />
            <span>{uploading ? 'Processing PDF...' : 'Upload PDF'}</span>
            <input
              type="file"
              accept=".pdf"
              className="hidden"
              onChange={handleFileUpload}
              disabled={uploading}
            />
          </label>
        </div>
      </div>

      {uploadError && (
        <div className="p-3 mb-6 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{uploadError}</span>
        </div>
      )}

      {/* Search Bar */}
      <div className="mb-6 relative">
        <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
        <input
          type="text"
          placeholder="Search documents by title or filename..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full pl-10 pr-4 py-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-200 placeholder-slate-500 text-sm focus:outline-none focus:border-teal-400"
        />
      </div>

      {/* Document Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-lg">
        {loading ? (
          <div className="p-8 text-center text-slate-400 text-sm">Loading document repository...</div>
        ) : filteredDocs.length === 0 ? (
          <div className="p-12 text-center text-slate-500 text-sm">
            No documents found. Click 'Upload PDF' to ingest your first lecture slide or assignment.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-950/60 border-b border-slate-800 text-xs uppercase text-slate-400">
                <tr>
                  <th className="px-6 py-3.5 w-10"></th>
                  <th className="px-6 py-3.5">Document</th>
                  <th className="px-6 py-3.5">Pages & Size</th>
                  <th className="px-6 py-3.5">SHA-256 Digest</th>
                  <th className="px-6 py-3.5">Protected Editions</th>
                  <th className="px-6 py-3.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-300">
                {filteredDocs.map((doc) => {
                  const isExpanded = !!expandedDocIds[doc.id];
                  const hasRecords = doc.watermark_records && doc.watermark_records.length > 0;
                  return (
                    <React.Fragment key={doc.id}>
                      <tr className="hover:bg-slate-800/40 transition">
                        <td className="px-4 py-4 text-center">
                          {hasRecords ? (
                            <button
                              onClick={() => toggleExpand(doc.id)}
                              className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-white transition"
                              title={isExpanded ? "Collapse editions" : "Expand watermarked editions"}
                            >
                              {isExpanded ? <ChevronDown className="w-4 h-4 text-teal-400" /> : <ChevronRight className="w-4 h-4" />}
                            </button>
                          ) : (
                            <span className="w-4 h-4 inline-block" />
                          )}
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-3">
                            <FileText className="w-5 h-5 text-teal-400 shrink-0" />
                            <div>
                              <div className="font-semibold text-white">{doc.title}</div>
                              <div className="text-xs text-slate-400">{doc.original_filename}</div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-xs text-slate-300">
                          {doc.page_count} pages • {(doc.file_size_bytes / 1024).toFixed(1)} KB
                        </td>
                        <td className="px-6 py-4">
                          <span className="font-mono text-xs text-slate-400">
                            {doc.original_sha256.substring(0, 14)}...
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <button
                            onClick={() => hasRecords && toggleExpand(doc.id)}
                            className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border transition ${
                              hasRecords 
                                ? 'bg-teal-500/10 text-teal-300 border-teal-500/30 hover:bg-teal-500/20 cursor-pointer' 
                                : 'bg-slate-800/40 text-slate-500 border-slate-700/40'
                            }`}
                          >
                            <ShieldCheck className="w-3.5 h-3.5" /> {doc.watermark_records_count || 0} Edition(s)
                            {hasRecords && (isExpanded ? <ChevronDown className="w-3 h-3 ml-0.5" /> : <ChevronRight className="w-3 h-3 ml-0.5" />)}
                          </button>
                        </td>
                        <td className="px-6 py-4 text-right space-x-2">
                          <button
                            onClick={() => { setSelectedDoc(doc); setWmSuccess(null); }}
                            className="px-3 py-1.5 rounded-lg bg-teal-500/10 hover:bg-teal-500/20 text-teal-300 border border-teal-500/30 text-xs font-semibold transition"
                          >
                            Apply Watermark
                          </button>
                          <button
                            onClick={() => handleViewPdf(`/documents/${doc.id}/download-original`)}
                            className="p-2 inline-block rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition"
                            title="View Original in Browser"
                          >
                            <ExternalLink className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => handleDownloadFile(`/documents/${doc.id}/download-original`, doc.original_filename)}
                            className="p-2 inline-block rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition"
                            title="Download Original PDF"
                          >
                            <Download className="w-4 h-4" />
                          </button>
                        </td>
                      </tr>

                      {/* Watermarked Editions Accordion Row */}
                      {isExpanded && hasRecords && (
                        <tr className="bg-slate-950/80 border-b border-slate-800">
                          <td colSpan={6} className="px-8 py-4">
                            <div className="space-y-2">
                              <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-2">
                                <Layers className="w-3.5 h-3.5 text-teal-400" />
                                Protected Watermarked Editions ({doc.watermark_records.length})
                              </div>
                              <div className="grid grid-cols-1 gap-2">
                                {doc.watermark_records.map((wm: any) => (
                                  <div
                                    key={wm.id}
                                    className="p-3 bg-slate-900 border border-slate-800 rounded-xl flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs"
                                  >
                                    <div className="space-y-1">
                                      <div className="flex items-center gap-2">
                                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                                          wm.watermark_type === 'visible' 
                                            ? 'bg-amber-500/10 text-amber-300 border border-amber-500/20' 
                                            : 'bg-indigo-500/10 text-indigo-300 border border-indigo-500/20'
                                        }`}>
                                          {wm.watermark_type}
                                        </span>
                                        <span className="font-semibold text-white">{wm.payload_text}</span>
                                        {wm.recipient_identifier && (
                                          <span className="text-slate-400">• Recipient: <span className="text-teal-300 font-mono">{wm.recipient_identifier}</span></span>
                                        )}
                                      </div>
                                      <div className="text-[11px] text-slate-400 font-mono flex items-center gap-3">
                                        <span>Size: {(wm.protected_file_size_bytes / 1024).toFixed(1)} KB</span>
                                        <span>SHA: {wm.protected_sha256?.substring(0, 12)}...</span>
                                        <span>Manifest: {wm.manifest_id}</span>
                                      </div>
                                    </div>

                                    <div className="flex items-center gap-2 shrink-0">
                                      <button
                                        onClick={() => handleViewPdf(`/watermarks/records/${wm.id}/download`)}
                                        className="px-2.5 py-1.5 rounded-lg bg-teal-500/10 hover:bg-teal-500/20 border border-teal-500/30 text-teal-300 font-medium flex items-center gap-1.5 transition"
                                        title="View Watermarked PDF in Browser"
                                      >
                                        <ExternalLink className="w-3.5 h-3.5" /> View PDF
                                      </button>
                                      <button
                                        onClick={() => handleDownloadFile(`/watermarks/records/${wm.id}/download`, `AquaMark_Secured_${doc.original_filename}`)}
                                        className="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-medium flex items-center gap-1.5 transition"
                                        title="Download Protected PDF"
                                      >
                                        <Download className="w-3.5 h-3.5" /> Download
                                      </button>
                                      <button
                                        onClick={() => handleDownloadFile(`/watermarks/records/${wm.id}/manifest`, `manifest_${wm.manifest_id}.json`)}
                                        className="px-2 py-1.5 rounded-lg bg-slate-950 hover:bg-slate-800 border border-slate-700 text-slate-400 hover:text-white transition"
                                        title="Download JSON Manifest"
                                      >
                                        <FileCheck className="w-3.5 h-3.5 text-teal-400" /> Manifest
                                      </button>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          </td>
                        </tr>
                      )}
                    </React.Fragment>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Watermark Generation Modal */}
      {selectedDoc && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl">
            <h3 className="text-xl font-bold text-white mb-2">Apply Cryptographic Watermark</h3>
            <p className="text-xs text-slate-400 mb-6">
              Embed watermarks and generate an Ed25519-signed provenance manifest for <span className="text-teal-400 font-semibold">{selectedDoc.original_filename}</span>.
            </p>

            {wmSuccess ? (
              <div className="p-5 rounded-xl bg-teal-500/10 border border-teal-500/30 text-teal-300 text-sm mb-4 space-y-3">
                <div className="flex items-center gap-2 font-semibold text-base text-teal-300">
                  <CheckCircle2 className="w-5 h-5 text-teal-400" /> Protected Document Generated!
                </div>
                <div className="text-xs text-slate-300 space-y-1 bg-slate-950/60 p-3 rounded-lg border border-slate-800 font-mono">
                  <div><strong className="text-slate-400">Record ID:</strong> {wmSuccess.id}</div>
                  <div><strong className="text-slate-400">Manifest:</strong> {wmSuccess.manifest_id}</div>
                  <div><strong className="text-slate-400">Algorithm:</strong> {wmSuccess.watermark_algorithm}</div>
                  <div><strong className="text-slate-400">Protected SHA:</strong> {wmSuccess.protected_sha256?.substring(0, 16)}...</div>
                </div>

                <div className="pt-2 flex flex-col sm:flex-row gap-2">
                  <button
                    onClick={() => handleViewPdf(`/watermarks/records/${wmSuccess.id}/download`)}
                    className="flex-1 py-2 px-3 rounded-lg bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold text-xs flex items-center justify-center gap-1.5 transition"
                  >
                    <ExternalLink className="w-4 h-4" /> View Watermarked PDF
                  </button>
                  <button
                    onClick={() => handleDownloadFile(`/watermarks/records/${wmSuccess.id}/download`, `AquaMark_Secured_${selectedDoc.original_filename}`)}
                    className="flex-1 py-2 px-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs flex items-center justify-center gap-1.5 transition"
                  >
                    <Download className="w-4 h-4" /> Download PDF
                  </button>
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={() => handleDownloadFile(`/watermarks/records/${wmSuccess.id}/manifest`, `manifest_${wmSuccess.manifest_id}.json`)}
                    className="flex-1 py-1.5 px-3 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs flex items-center justify-center gap-1.5 transition"
                  >
                    <FileCheck className="w-3.5 h-3.5 text-teal-400" /> Download Signed Manifest
                  </button>
                  <button
                    onClick={() => setSelectedDoc(null)}
                    className="py-1.5 px-4 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold"
                  >
                    Close
                  </button>
                </div>
              </div>
            ) : (
              <form onSubmit={handleApplyWatermark} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1.5">Watermark Technique</label>
                  <div className="grid grid-cols-2 gap-3">
                    <button
                      type="button"
                      onClick={() => setWmType('visible')}
                      className={`p-3 rounded-xl border text-left transition ${
                        wmType === 'visible' 
                          ? 'border-teal-500 bg-teal-500/10 text-white' 
                          : 'border-slate-800 bg-slate-950 text-slate-400'
                      }`}
                    >
                      <div className="font-semibold text-xs text-white">Visible Overlay</div>
                      <div className="text-[11px] text-slate-400 mt-1">Rotated text across all pages</div>
                    </button>
                    <button
                      type="button"
                      onClick={() => setWmType('invisible_dct')}
                      className={`p-3 rounded-xl border text-left transition ${
                        wmType === 'invisible_dct' 
                          ? 'border-teal-500 bg-teal-500/10 text-white' 
                          : 'border-slate-800 bg-slate-950 text-slate-400'
                      }`}
                    >
                      <div className="font-semibold text-xs text-white">Invisible DCT</div>
                      <div className="text-[11px] text-slate-400 mt-1">Mid-freq coefficient modulation</div>
                    </button>
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1.5">Watermark Payload / Text</label>
                  <input
                    type="text"
                    required
                    value={wmText}
                    onChange={(e) => setWmText(e.target.value)}
                    className="w-full px-3.5 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white text-sm focus:outline-none focus:border-teal-400"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                    Recipient Identifier <span className="text-slate-500 font-normal">(Optional, for forensic tracing)</span>
                  </label>
                  <input
                    type="text"
                    placeholder="e.g. STUDENT-2026-904"
                    value={recipientId}
                    onChange={(e) => setRecipientId(e.target.value)}
                    className="w-full px-3.5 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white text-sm focus:outline-none focus:border-teal-400"
                  />
                </div>

                <div className="pt-4 flex items-center justify-end gap-3 border-t border-slate-800">
                  <button
                    type="button"
                    onClick={() => setSelectedDoc(null)}
                    className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={applyingWm}
                    className="px-5 py-2 rounded-lg bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold text-xs shadow-md shadow-teal-500/20 disabled:opacity-50"
                  >
                    {applyingWm ? 'Watermarking & Signing...' : 'Generate Protected Copy'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
