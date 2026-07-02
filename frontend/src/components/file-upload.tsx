"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, X, Camera } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

interface FileUploadProps {
  value?: string;
  onChange: (url: string) => void;
  onRemove: () => void;
  disabled?: boolean;
}

export function FileUpload({ value, onChange, onRemove, disabled }: FileUploadProps) {
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      if (acceptedFiles.length === 0) return;
      
      const file = acceptedFiles[0];
      
      // Check file size (5MB limit)
      if (file.size > 5 * 1024 * 1024) {
        alert("File size must be less than 5MB");
        return;
      }

      // Check file type
      if (!file.type.startsWith("image/")) {
        alert("Only image files are allowed");
        return;
      }

      setIsUploading(true);
      
      try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001'}/api/upload`, {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          throw new Error("Upload failed");
        }

        const result = await response.json();
        onChange(result.url);
      } catch (error) {
        console.error("Upload error:", error);
        alert("Failed to upload file");
      } finally {
        setIsUploading(false);
      }
    },
    [onChange]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/*": [".jpeg", ".jpg", ".png", ".gif", ".webp"],
    },
    multiple: false,
    disabled: disabled || isUploading,
  });

  if (value) {
    return (
      <Card className="w-fit">
        <CardContent className="p-2">
          <div className="relative">
            <Avatar className="w-20 h-20">
              <AvatarImage src={value} alt="Profile" />
              <AvatarFallback>Profile</AvatarFallback>
            </Avatar>
            <Button
              type="button"
              variant="destructive"
              size="icon"
              className="absolute -top-2 -right-2 w-6 h-6 rounded-full"
              onClick={onRemove}
              disabled={disabled}
            >
              <X className="w-3 h-3" />
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-fit">
      <CardContent className="p-2">
        <div
          {...getRootProps()}
          className={`
            border-2 border-dashed rounded-lg p-4 cursor-pointer transition-colors
            ${isDragActive ? "border-primary bg-primary/5" : "border-gray-300 hover:border-gray-400"}
            ${isUploading ? "opacity-50 cursor-not-allowed" : ""}
          `}
        >
          <input {...getInputProps()} />
          <div className="flex flex-col items-center justify-center gap-2 text-sm">
            {isUploading ? (
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
            ) : (
              <Camera className="w-6 h-6 text-gray-400" />
            )}
            {isUploading ? (
              <span>Uploading...</span>
            ) : isDragActive ? (
              <span>Drop the image here</span>
            ) : (
              <div className="text-center">
                <span className="text-gray-600">Click to upload or drag and drop</span>
                <br />
                <span className="text-gray-400">PNG, JPG, GIF up to 5MB</span>
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}