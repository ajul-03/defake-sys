import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Crosshair, Upload, FileVideo } from 'lucide-react';
import { cn } from '../lib/utils';

const UploadDropzone = ({ onFileSelect }) => {
    const onDrop = useCallback(acceptedFiles => {
        if (acceptedFiles?.length > 0) {
            onFileSelect(acceptedFiles[0]);
        }
    }, [onFileSelect]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'video/mp4': ['.mp4'],
            'video/x-msvideo': ['.avi'],
            'video/quicktime': ['.mov']
        },
        maxFiles: 1
    });

    return (
        <div
            {...getRootProps()}
            className={cn(
                "relative w-full border-2 border-dashed bg-black/50 p-8 text-center cursor-pointer transition-all duration-300 group",
                isDragActive ? "border-[#00ffff] bg-[#00ffff]/10" : "border-[#64748b]/50 hover:border-[#00ffff]/50"
            )}
        >
            <input {...getInputProps()} />
            
            {/* Corner Targeting Rectangles matching theme */}
            <div className="absolute top-0 left-0 w-3 h-3 border-t-2 border-l-2 border-[#00ffff] opacity-50 transition-all group-hover:scale-110 group-hover:opacity-100" />
            <div className="absolute top-0 right-0 w-3 h-3 border-t-2 border-r-2 border-[#00ffff] opacity-50 transition-all group-hover:scale-110 group-hover:opacity-100" />
            <div className="absolute bottom-0 left-0 w-3 h-3 border-b-2 border-l-2 border-[#00ffff] opacity-50 transition-all group-hover:scale-110 group-hover:opacity-100" />
            <div className="absolute bottom-0 right-0 w-3 h-3 border-b-2 border-r-2 border-[#00ffff] opacity-50 transition-all group-hover:scale-110 group-hover:opacity-100" />

            <div className="flex flex-col items-center justify-center space-y-4">
                <div className={cn(
                    "p-4 rounded-full border border-[#00ffff]/30 bg-black transition-colors duration-300 relative",
                    isDragActive ? "text-[#00ffff] shadow-[0_0_15px_#00ffff]" : "text-[#64748b] group-hover:text-[#00ffff]/70 group-hover:border-[#00ffff]/50"
                )}>
                    {isDragActive ? <Crosshair className="w-8 h-8 animate-spin-slow" /> : <Upload className="w-8 h-8" />}
                    
                    {/* Inner glowing pulse on hover */}
                     <div className="absolute inset-0 rounded-full bg-[#00ffff]/10 blur-md opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>

                <div className="font-mono">
                    <p className={cn(
                        "text-sm font-bold tracking-widest uppercase transition-colors",
                        isDragActive ? "text-[#00ffff] glow-text" : "text-[#e2e8f0]"
                    )}>
                        {isDragActive ? "LOCK SECURED: DROP UPLOAD" : "INITIALIZE UPLOAD SEQUENCE"}
                    </p>
                    <p className="text-xs text-[#64748b] mt-2 tracking-wider">
                        DRAG & DROP OR [ CLICK TO TARGET ]
                    </p>
                    <p className="text-[10px] text-[#64748b]/50 mt-4 uppercase">
                        SUPPORTED MODULES: .MP4, .AVI, .MOV (MAX 50MB)
                    </p>
                </div>
            </div>
        </div>
    );
};

export default UploadDropzone;
