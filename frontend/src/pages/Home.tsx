import React from 'react';
import { Link } from 'react-router-dom';
import { 
  ShieldCheck, 
  FileCheck2, 
  Binary, 
  Lock, 
  CheckCircle2, 
  ArrowRight, 
  Fingerprint,
  Layers,
  Database
} from 'lucide-react';

export const Home: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 lg:py-28 border-b border-slate-800 bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center max-w-3xl mx-auto">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-teal-500/30 bg-teal-500/10 text-teal-300 text-xs font-semibold uppercase tracking-wider mb-6">
              <ShieldCheck className="w-4 h-4" /> Cryptographic Integrity & Watermarking
            </div>
            <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white mb-6">
              Protect Every Document. <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-cyan-300">
                Verify Every Claim.
              </span>
            </h1>
            <p className="text-lg text-slate-300 mb-8 leading-relaxed">
              Robust digital watermarking platform tailored for university lecture notes, exam papers, and course content.
              Combines DCT spread-spectrum steganography with Ed25519 digital signatures and SHA-256 provenance manifests.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                to="/register"
                className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold transition shadow-lg shadow-teal-500/20 flex items-center justify-center gap-2"
              >
                Start Protecting Content <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                to="/verify"
                className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold border border-slate-700 transition flex items-center justify-center gap-2"
              >
                <FileCheck2 className="w-5 h-5 text-teal-400" /> Verify Existing Document
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Distinction Section: Watermark vs Signature vs Hash */}
      <section className="py-16 bg-slate-900 border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h2 className="text-2xl font-bold text-white tracking-tight">The Three Pillars of Document Security</h2>
            <p className="text-sm text-slate-400 mt-2">
              AquaMark harmonizes three distinct mathematical concepts rather than treating them as interchangeable.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 rounded-2xl bg-slate-950 border border-slate-800 hover:border-slate-700 transition">
              <div className="w-12 h-12 rounded-xl bg-teal-950 border border-teal-800 flex items-center justify-center text-teal-400 mb-4">
                <Binary className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">1. Digital Watermarking</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                Embeds perceptible or imperceptible signals (DCT mid-frequency) directly into the carrier media. Remains recoverable even when the file structure is transformed, recompressed, or printed.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-slate-950 border border-slate-800 hover:border-slate-700 transition">
              <div className="w-12 h-12 rounded-xl bg-cyan-950 border border-cyan-800 flex items-center justify-center text-cyan-400 mb-4">
                <Fingerprint className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">2. SHA-256 Hashing</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                Provides a deterministic mathematical digest. Yields complete sensitivity to bit-level alterations, enabling instant identification of byte-for-byte unmodified originals.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-slate-950 border border-slate-800 hover:border-slate-700 transition">
              <div className="w-12 h-12 rounded-xl bg-indigo-950 border border-indigo-800 flex items-center justify-center text-indigo-400 mb-4">
                <Lock className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">3. Ed25519 Signatures</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                Binds the document digest, timestamp, and author identity to an asymmetric cryptographic keypair. Proves authenticity without revealing private signing credentials.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="py-20 bg-slate-950">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-3xl font-extrabold text-white">Full-Stack Forensic Capabilities</h2>
            <p className="text-slate-400 mt-3 text-sm">
              Engineered specifically for academic institutions protecting intellectual property.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/50">
              <CheckCircle2 className="w-5 h-5 text-teal-400 mb-3" />
              <h4 className="font-semibold text-white mb-1">Visible PDF Markings</h4>
              <p className="text-xs text-slate-400">Rotated, customized opacity overlays across all pages preserving vector geometry.</p>
            </div>
            <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/50">
              <CheckCircle2 className="w-5 h-5 text-teal-400 mb-3" />
              <h4 className="font-semibold text-white mb-1">DCT Steganography</h4>
              <p className="text-xs text-slate-400">Mid-frequency coefficient modulation for invisible, JPEG-resilient watermarks.</p>
            </div>
            <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/50">
              <CheckCircle2 className="w-5 h-5 text-teal-400 mb-3" />
              <h4 className="font-semibold text-white mb-1">Recipient Attribution</h4>
              <p className="text-xs text-slate-400">Embed student or recipient-specific pseudonymous IDs for leakage traceability.</p>
            </div>
            <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/50">
              <CheckCircle2 className="w-5 h-5 text-teal-400 mb-3" />
              <h4 className="font-semibold text-white mb-1">Robustness Lab</h4>
              <p className="text-xs text-slate-400">Empirically evaluate watermark survival against compression, resizing, and noise.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
