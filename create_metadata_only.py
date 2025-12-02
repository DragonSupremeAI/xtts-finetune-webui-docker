#!/usr/bin/env python3
"""
Metadata-only dataset creation script for XTTS training.
This script generates JSON/CSV metadata files without modifying the original audio files.
Perfect for when you have pre-processed audio files and just need the metadata mapping.
"""

import os
import sys
import argparse
import json
from pathlib import Path
from faster_whisper import WhisperModel
import torch
import pandas as pd

# Add the utils directory to the path to import formatter
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
from formatter import format_audio_metadata_only, list_audios

def main():
    parser = argparse.ArgumentParser(description='Create metadata-only dataset for XTTS training')
    parser.add_argument('--input_dir', type=str, required=True, 
                        help='Directory containing pre-processed audio files')
    parser.add_argument('--output_dir', type=str, required=True,
                        help='Output directory for metadata files')
    parser.add_argument('--language', type=str, default='en',
                        help='Language code (default: en)')
    parser.add_argument('--whisper_model', type=str, default='base',
                        help='Whisper model size (default: base)')
    parser.add_argument('--speaker_name', type=str, default='coqui',
                        help='Speaker name for metadata (default: coqui)')
    parser.add_argument('--eval_percentage', type=float, default=0.15,
                        help='Percentage of data for evaluation (default: 0.15)')
    parser.add_argument('--device', type=str, default='auto',
                        help='Device to use (auto, cuda, cpu) (default: auto)')
    
    args = parser.parse_args()
    
    # Validate input directory
    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist!")
        sys.exit(1)
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Determine device
    if args.device == 'auto':
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = args.device
    
    print(f"Using device: {device}")
    print(f"Loading Whisper model: {args.whisper_model}")
    
    # Load Whisper model
    try:
        compute_type = "float16" if device == "cuda" else "float32"
        asr_model = WhisperModel(args.whisper_model, device=device, compute_type=compute_type)
    except Exception as e:
        print(f"Error loading Whisper model: {e}")
        sys.exit(1)
    
    # Find audio files
    print(f"Scanning for audio files in: {args.input_dir}")
    audio_files = list(list_audios(args.input_dir))
    
    if not audio_files:
        print("No audio files found!")
        sys.exit(1)
    
    print(f"Found {len(audio_files)} audio files")
    
    # Process metadata
    print("Generating metadata files...")
    try:
        train_csv, eval_csv, audio_total_size = format_audio_metadata_only(
            audio_files=audio_files,
            asr_model=asr_model,
            target_language=args.language,
            out_path=args.output_dir,
            eval_percentage=args.eval_percentage,
            speaker_name=args.speaker_name
        )
        
        if train_csv and eval_csv:
            print(f"\n✅ Metadata generation completed!")
            print(f"📁 Output directory: {args.output_dir}")
            print(f"📊 Total audio duration: {audio_total_size:.2f} seconds")
            print(f"📄 Train metadata: {train_csv}")
            print(f"📄 Eval metadata: {eval_csv}")
            
            # Show summary
            train_df = pd.read_csv(train_csv, sep='|')
            eval_df = pd.read_csv(eval_csv, sep='|')
            print(f"📈 Train samples: {len(train_df)}")
            print(f"📈 Eval samples: {len(eval_df)}")
            
            # Also mention JSON files
            train_json = train_csv.replace('.csv', '.json')
            eval_json = eval_csv.replace('.csv', '.json')
            if os.path.exists(train_json):
                print(f"📄 Train JSON: {train_json}")
            if os.path.exists(eval_json):
                print(f"📄 Eval JSON: {eval_json}")
                
        else:
            print("❌ Failed to generate metadata!")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error during processing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()