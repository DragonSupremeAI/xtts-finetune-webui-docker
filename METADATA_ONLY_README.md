# Metadata-Only Dataset Creation for XTTS

This script allows you to create JSON/CSV metadata files for XTTS training without modifying your original audio files. Perfect when you have pre-processed audio files and just need the transcription mapping.

## Usage

### Command Line

```bash
python create_metadata_only.py \
    --input_dir /path/to/your/preprocessed/audio \
    --output_dir /path/to/output/metadata \
    --language en \
    --whisper_model base \
    --speaker_name your_speaker_name
```

### Parameters

- `--input_dir`: Directory containing your pre-processed audio files (.wav, .mp3, .flac)
- `--output_dir`: Where to save the metadata files
- `--language`: Language code (default: 'en')
- `--whisper_model`: Whisper model size (default: 'base')
- `--speaker_name`: Speaker name for metadata (default: 'coqui')
- `--eval_percentage`: Percentage for evaluation split (default: 0.15)
- `--device`: Device to use (auto, cuda, cpu) (default: 'auto')

### Output Files

The script generates:
- `metadata_train.csv` - Training metadata in CSV format
- `metadata_eval.csv` - Evaluation metadata in CSV format
- `metadata_train.json` - Training metadata in JSON format
- `metadata_eval.json` - Evaluation metadata in JSON format
- `lang.txt` - Language file

### Example

```bash
python create_metadata_only.py \
    --input_dir /home/user/cleaned_audio \
    --output_dir /home/user/xtts_dataset \
    --language en \
    --whisper_model base \
    --speaker_name john_doe
```

## Integration with Existing Workflow

1. Process your audio files with your own scripts (denoising, segmentation, etc.)
2. Run this script to generate metadata files
3. Use the generated metadata files for XTTS training

## Key Differences from Regular Dataset Creation

- ✅ **No audio modification**: Original files remain untouched
- ✅ **No audio segmentation**: Uses your existing audio structure
- ✅ **Faster processing**: Only transcribes, no audio processing
- ✅ **JSON output**: Both CSV and JSON formats for flexibility
- ✅ **Original paths**: Metadata points to your original audio files

## Metadata Format

The generated JSON files contain entries like:
```json
[
  {
    "audio_file": "/path/to/your/audio/file1.wav",
    "text": "Transcribed text here",
    "speaker_name": "your_speaker_name"
  },
  ...
]
```

This allows you to use your pre-processed audio files directly with XTTS training workflows.