import React from 'react';
import { ShieldCheck, BookOpen, Lock, Terminal, Cpu, CheckCircle2 } from 'lucide-react';

export const About: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-14">
      <div className="mb-12 text-center">
        <h1 className="text-3xl font-extrabold text-white tracking-tight">Academic & Cryptographic Specifications</h1>
        <p className="text-sm text-slate-400 mt-2">
          Project identity, threat modeling, algorithm specifications, and research limitations.
        </p>
      </div>

      <div className="space-y-8">
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h2 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-teal-400" /> Academic Project Identity
          </h2>
          <div className="text-sm text-slate-300 space-y-2">
            <p><strong>Official Title:</strong> Robust Digital Watermarking for Protection of Electronic Course Content</p>
            <p><strong>Platform Name:</strong> AquaMark</p>
            <p><strong>Academic Domain:</strong> Applied Cryptography, Steganography, Digital Document Forensics</p>
            <p><strong>Primary Objective:</strong> Authenticate ownership, detect tampering, and trace leaks in PDF course materials without relying exclusively on brittle byte-level hashing or non-verifiable cosmetic stamps.</p>
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h2 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
            <Lock className="w-5 h-5 text-teal-400" /> Implemented Cryptographic Controls
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-slate-300">
            <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">
              <strong className="text-white block mb-1">Ed25519 Canonical Manifests</strong>
              High-security elliptic curve digital signatures signing canonical JSON manifest structures to prove provenance.
            </div>
            <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">
              <strong className="text-white block mb-1">HMAC-SHA-256 Record Integrity</strong>
              HMAC validation ensuring that the pairing between original and protected document hashes cannot be forged.
            </div>
            <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">
              <strong className="text-white block mb-1">Argon2id Password Security</strong>
              State-of-the-art memory-hard key derivation protecting user passwords from GPU-accelerated dictionary attacks.
            </div>
            <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">
              <strong className="text-white block mb-1">Tamper-Evident Hash Chaining</strong>
              Every audit action is chained to the SHA-256 hash of previous events, creating an immutable sequence.
            </div>
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h2 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
            <Cpu className="w-5 h-5 text-teal-400" /> Watermarking Mathematics: Discrete Cosine Transform (DCT)
          </h2>
          <p className="text-xs text-slate-300 leading-relaxed mb-3">
            To embed imperceptible watermarks resilient to raster recompression, AquaMark transforms 8×8 pixel blocks in the Luminance (Y) channel into the frequency domain:
          </p>
          <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 text-xs font-mono text-teal-300 mb-3">
            {"F(u,v) = 1/4 * C(u) C(v) * sum sum f(x,y) cos[(2x+1)u*pi / 16] cos[(2y+1)v*pi / 16]"}
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            Bits are embedded into mid-frequency coefficient pairs <code className="text-teal-400">(3,2)</code> and <code className="text-teal-400">(2,3)</code>. Mid-frequency bands are selected because low frequencies hold primary visual energy (causing perceptible distortion if modified), while high frequencies are eliminated during lossy JPEG compression.
          </p>
        </div>

        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h2 className="text-lg font-bold text-white mb-3 flex items-center gap-2">
            <Terminal className="w-5 h-5 text-amber-400" /> Technical Limitations & Honest Boundaries
          </h2>
          <ul className="list-disc pl-5 text-xs text-slate-300 space-y-1.5">
            <li>Digital watermarking provides leak deterrence and source attribution, not absolute physical copy prevention.</li>
            <li>Aggressive cropping (removing over 30% of content) or severe geometric warping impairs payload extraction.</li>
            <li>A valid Ed25519 digital signature establishes cryptographic record integrity; it does not replace legal copyright arbitration.</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
