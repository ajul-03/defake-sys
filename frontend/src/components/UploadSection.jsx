import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, FileVideo } from 'lucide-react';

const UploadSection = ({ onFileSelect }) => {
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
        <div id="demo" className="py-20 px-4">
            <div
                className="max-w-3xl mx-auto text-center"
            >
                <h2 className="text-3xl font-bold mb-8">Analyze Your Video</h2>

                <div
                    {...getRootProps()}
                    className={`glass-card p-12 rounded-2xl border-2 border-dashed cursor-pointer transition-all ${isDragActive ? 'border-primary bg-primary/5' : 'border-gray-700 hover:border-gray-500'
                        }`}
                >
                    <input {...getInputProps()} />
                    <div className="flex flex-col items-center space-y-4">
                        <div className="p-4 rounded-full bg-gray-800">
                            {isDragActive ? (
                                <FileVideo className="w-10 h-10 text-primary" />
                            ) : (
                                <UploadCloud className="w-10 h-10 text-gray-400" />
                            )}
                        </div>
                        <div>
                            <p className="text-xl font-medium text-white">
                                {isDragActive ? 'Drop your video here' : 'Drag & Drop your video here'}
                            </p>
                            <p className="text-gray-400 mt-2">
                                or click to browse (MP4, AVI, MOV)
                            </p>
                        </div>
                        <p className="text-xs text-gray-500 mt-4">
                            Max file size: 50MB
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UploadSection;
