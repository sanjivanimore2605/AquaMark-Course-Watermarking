import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { 
  Cpu, 
  Play, 
  CheckCircle2, 
  XCircle, 
  Sliders, 
  Activity, 
  Layers,
  Info
} from 'lucide-react';

export const Lab: React.FC = () => {
  const [records, setRecords] = useState<any[]>([]);
  const [selectedRecordId, setSelectedRecordId] = useState('');
  const [transType, setTransType] = useState('jpeg_compression');
  const [intensity, setIntensity] = useState(75);
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<any | null>(null);

  useEffect(() => {
    const fetchDocs = async () => {
      try {
        const res = await api.get('/documents');
        // Extract watermark records
        const allRecords: any[] = [];
        res.data.forEach((d: any) => {
          if (d.watermark_records && d.watermark_records.length > 0) {
            d.watermark_records.forEach((wm: any) => {
              allRecords.push({
                id: wm.id,
                label: `${d.title} (${wm.watermark_type.toUpperCase()} - ${wm.payload_text})`
              });
            });
          }
        });
        setRecords(allRecords);
        if (allRecords.length > 0) {
          setSelectedRecordId(allRecords[0].id);
        }
      } catch (err) {
        console.error(err);
      }
    };
    fetchDocs();
  }, []);

  const handleRunTrial = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedRecordId) {
      alert('Please select a watermarked document edition.');
      return;
    }

    setRunning(true);
    setResult(null);

    try {
      const res = await api.post('/experiments/run', {
        watermark_record_id: selectedRecordId,
        transformation_type: transType,
        intensity: Number(intensity)
      });
      setResult(res.data);
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Experiment trial failed.');
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-12">
      <div className="text-center mb-10">
        <div className="inline-flex p-3 bg-teal-500/10 rounded-2xl text-teal-400 mb-3 border border-teal-500/20">
          <Cpu className="w-8 h-8" />
        </div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">Robustness Testing Laboratory</h1>
        <p className="text-sm text-slate-400 mt-2 max-w-xl mx-auto">
          Empirically test discrete cosine transform (DCT) watermark resilience against real-world image degradation, recompression, and noise attacks.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
        {/* Configuration Panel */}
        <div className="md:col-span-1 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
          <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
            <Sliders className="w-4 h-4 text-teal-400" /> Trial Parameters
          </h3>

          <form onSubmit={handleRunTrial} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Target Watermarked Edition</label>
              <select
                required
                value={selectedRecordId}
                onChange={(e) => setSelectedRecordId(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-xs text-white focus:outline-none focus:border-teal-400"
              >
                <option value="">Select a watermarked edition...</option>
                {records.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Distortion Vector</label>
              <select
                value={transType}
                onChange={(e) => {
                  const t = e.target.value;
                  setTransType(t);
                  if (t === 'jpeg_compression') setIntensity(70);
                  if (t === 'resize') setIntensity(0.75);
                  if (t === 'gaussian_noise') setIntensity(15);
                  if (t === 'crop') setIntensity(0.05);
                }}
                className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-xs text-white focus:outline-none focus:border-teal-400"
              >
                <option value="jpeg_compression">JPEG Lossy Compression</option>
                <option value="resize">Geometric Downscaling / Upscaling</option>
                <option value="gaussian_noise">Additive Gaussian Noise</option>
                <option value="crop">Border Cropping & Aspect Resampling</option>
              </select>
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-300 mb-1.5">
                <span>Distortion Intensity</span>
                <span className="text-teal-400 font-mono">{intensity}</span>
              </div>
              <input
                type="range"
                min={transType === 'resize' ? 0.25 : transType === 'crop' ? 0.01 : 10}
                max={transType === 'resize' ? 0.95 : transType === 'crop' ? 0.20 : 95}
                step={transType === 'resize' || transType === 'crop' ? 0.01 : 1}
                value={intensity}
                onChange={(e) => setIntensity(Number(e.target.value))}
                className="w-full accent-teal-400"
              />
            </div>

            <button
              type="submit"
              disabled={running}
              className="w-full py-2.5 rounded-lg bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold transition flex items-center justify-center gap-2 text-xs shadow-md shadow-teal-500/20 disabled:opacity-50 mt-4"
            >
              {running ? 'Executing Trial...' : 'Execute Robustness Test'} <Play className="w-3.5 h-3.5" />
            </button>
          </form>
        </div>

        {/* Results Panel */}
        <div className="md:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-xl">
          <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
            <Activity className="w-4 h-4 text-cyan-400" /> Empirical Forensic Evaluation
          </h3>

          {result ? (
            <div className="space-y-6">
              <div className={`p-4 rounded-xl border flex items-center gap-3 ${
                result.payload_recovered
                  ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                  : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
              }`}>
                {result.payload_recovered ? (
                  <CheckCircle2 className="w-6 h-6 text-emerald-400 shrink-0" />
                ) : (
                  <XCircle className="w-6 h-6 text-rose-400 shrink-0" />
                )}
                <div>
                  <div className="font-bold text-sm">
                    {result.payload_recovered ? 'Watermark Successfully Recovered' : 'Payload Corrupted / Unrecovered'}
                  </div>
                  <div className="text-xs mt-0.5">
                    {result.payload_recovered
                      ? 'The mid-frequency DCT coefficients preserved sufficient energy to extract the complete preamble and payload.'
                      : 'Distortion intensity exceeded the error-correction threshold, degrading coefficient differences.'}
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <div className="text-[11px] text-slate-400">Peak Signal-to-Noise</div>
                  <div className="text-lg font-bold text-white mt-1">{result.psnr_db} dB</div>
                </div>

                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <div className="text-[11px] text-slate-400">Bit Error Rate (BER)</div>
                  <div className="text-lg font-bold text-white mt-1">{(result.bit_error_rate * 100).toFixed(1)}%</div>
                </div>

                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <div className="text-[11px] text-slate-400">Extracted Payload</div>
                  <div className="text-xs font-mono font-bold text-teal-400 mt-2 truncate">
                    {result.extracted_payload || 'None'}
                  </div>
                </div>

                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <div className="text-[11px] text-slate-400">Execution Time</div>
                  <div className="text-lg font-bold text-white mt-1">{result.execution_duration_ms} ms</div>
                </div>
              </div>
            </div>
          ) : (
            <div className="p-12 text-center text-slate-500 text-sm">
              Configure parameters on the left and click 'Execute Robustness Test' to generate empirical metrics.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
