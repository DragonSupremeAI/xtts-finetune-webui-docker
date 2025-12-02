# Simple Metadata Generator for Existing Audio Datasets

This script creates XTTS-compatible metadata files from your existing processed audio files and their transcription files. No audio processing or transcription - just maps existing files to XTTS format.

## Expected File Structure

Your input directory should contain:
```
your_audio_folder/
├── audio1.wav
├── audio1.txt    (contains transcription for audio1.wav)
├── audio2.wav
├── audio2.txt    (contains transcription for audio2.wav)
├── audio3.flac
├── audio3.txt    (contains transcription for audio3.flac)
└── ...
```

## Usage

```bash
python create_metadata_from_existing.py \
    --input_dir /path/to/your/processed/audio \
    --output_dir /path/to/output/metadata \
    --language en \
    --speaker_name your_speaker_name
```

### Parameters

- `--input_dir`: Directory containing your processed audio files AND their .txt transcription files
- `--output_dir`: Where to save the metadata files
- `--language`: Language code (default: 'en')
- `--speaker_name`: Speaker name for metadata (default: 'coqui')
- `--eval_percentage`: Percentage for evaluation split (default: 0.15)

### Output Files

The script generates:
- `metadata_train.csv` - Training metadata in CSV format
- `metadata_eval.csv` - Evaluation metadata in CSV format
- `metadata_train.json` - Training metadata in JSON format
- `metadata_eval.json` - Evaluation metadata in JSON format
- `lang.txt` - Language file

### Example

```bash
python create_metadata_from_existing.py \
    --input_dir /home/user/my_processed_audio \
    --output_dir /home/user/xtts_metadata \
    --language en \
    --speaker_name john_doe \
    --eval_percentage 0.1
```

## Key Features

- ✅ **Zero audio processing** - Uses your existing processed audio as-is
- ✅ **Zero transcription** - Uses your existing transcription files
- ✅ **Fast processing** - Just file mapping and text cleaning
- ✅ **Multiple formats** - Outputs both CSV and JSON
- ✅ **XTTS compatible** - Direct plug-and-play with XTTS training

## Metadata Format

The generated JSON files contain entries like:
```json
[
  {
    "audio_file": "/path/to/your/audio1.wav",
    "text": "This is the transcribed text from audio1.txt",
    "speaker_name": "your_speaker_name"
  },
  {
    "audio_file": "/path/to/your/audio2.wav", 
    "text": "This is the transcribed text from audio2.txt",
    "speaker_name": "your_speaker_name"
  }
]
```

## Integration with Your Workflow

1. Your existing scripts process audio (denoise, segment, etc.) → creates clean audio files
2. Your existing scripts create transcriptions → creates .txt files
3. Run this script → creates XTTS metadata files
4. Use metadata files with XTTS training

Perfect for when you have your own optimized audio processing pipeline and just need the metadata mapping!