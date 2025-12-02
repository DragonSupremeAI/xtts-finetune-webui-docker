#!/usr/bin/env python3
"""
Simple metadata generator for existing processed audio datasets.
This script creates JSON/CSV metadata files from your existing audio files and their transcription files.
No audio processing or transcription - just maps existing files to XTTS format.
"""

import os
import sys
import argparse
import json
from pathlib import Path
import pandas as pd

# Add the utils directory to the path to import formatter
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
from formatter import format_existing_dataset, list_audios

def main():
    parser = argparse.ArgumentParser(description='Create metadata from existing processed audio + transcription files')
    parser.add_argument('--input_dir', type=str, required=True, 
                        help='Directory containing processed audio files and their .txt transcription files')
    parser.add_argument('--output_dir', type=str, required=True,
                        help='Output directory for metadata files')
    parser.add_argument('--language', type=str, default='en',
                        help='Language code (default: en)')
    parser.add_argument('--speaker_name', type=str, default='coqui',
                        help='Speaker name for metadata (default: coqui)')
    parser.add_argument('--eval_percentage', type=float, default=0.15,
                        help='Percentage of data for evaluation (default: 0.15)')
    parser.add_argument('--transcript_extension', type=str, default='.txt',
                        help='Extension of the transcript files that pair with the audio (default: .txt)')
    
    args = parser.parse_args()
    
    # Validate input directory
    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist!")
        sys.exit(1)
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    print(f"Scanning for audio files in: {args.input_dir}")
    
    # Process metadata
    print("Generating metadata files from existing dataset...")
    try:
        train_csv, eval_csv, audio_total_size = format_existing_dataset(
            audio_dir=args.input_dir,
            target_language=args.language,
            out_path=args.output_dir,
            eval_percentage=args.eval_percentage,
            speaker_name=args.speaker_name,
            transcript_extension=args.transcript_extension
        )
        
        if train_csv and eval_csv:
            print(f"\n✅ Metadata generation completed!")
            print(f"📁 Input directory: {args.input_dir}")
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
                
            print(f"\n📋 Expected file structure in {args.input_dir}:")
            print(f"   audio1.wav")
            print(f"   audio1.txt  (contains transcription)")
            print(f"   audio2.wav")
            print(f"   audio2.txt  (contains transcription)")
            print(f"   ...")
                
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
