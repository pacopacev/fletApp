#!/usr/bin/env python3
"""
DEBUG Radio Stream Issues
"""

import subprocess
import tempfile
import json
import os
import requests
import time
from datetime import datetime

def debug_stream(stream_url, duration=20):
    """Debug each step of the process"""
    
    print(f"{'='*60}")
    print(f"DEBUGGING STREAM: {stream_url[:80]}...")
    print(f"{'='*60}")
    
    # Step 1: Capture audio
    print("\n1️⃣  CAPTURING AUDIO...")
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    audio_path = temp_file.name
    temp_file.close()
    
    try:
        # Capture with verbose output
        cmd = [
            'ffmpeg',
            '-i', stream_url,
            '-t', str(duration),
            '-ar', '11025',
            '-ac', '1',
            '-acodec', 'pcm_s16le',
            '-y',
            audio_path
        ]
        
        print(f"Running: {' '.join(cmd[:5])}...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration + 10)
        
        if result.returncode != 0:
            print(f"❌ FFmpeg error:")
            print(result.stderr[:500])
            return
        
        if os.path.exists(audio_path):
            size_kb = os.path.getsize(audio_path) / 1024
            print(f"✅ Captured: {size_kb:.1f} KB")
            
            # Play a snippet to check if it's audio (optional)
            play_audio = input("\nPlay 2 seconds of captured audio? (y/n): ").lower()
            if play_audio == 'y':
                os.system(f"ffplay -nodisp -autoexit -t 2 {audio_path} 2>/dev/null")
        else:
            print("❌ No audio file created")
            return
    
    except Exception as e:
        print(f"❌ Capture error: {e}")
        return
    
    # Step 2: Generate fingerprint
    print("\n2️⃣  GENERATING FINGERPRINT...")
    try:
        cmd = ['fpcalc', '-json', audio_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode != 0:
            print(f"❌ fpcalc error: {result.stderr}")
            return
        
        data = json.loads(result.stdout)
        duration = data.get('duration', 0)
        fingerprint = data.get('fingerprint', '')
        
        print(f"✅ Fingerprint generated:")
        print(f"   Duration: {duration:.1f}s")
        print(f"   Length: {len(fingerprint)} characters")
        print(f"   Sample (first 100 chars):")
        print(f"   {fingerprint[:100]}")
        print(f"   Sample (last 100 chars):")
        print(f"   {fingerprint[-100:]}")
        
        # Check fingerprint characteristics
        if len(fingerprint) < 100:
            print("⚠ Warning: Fingerprint is very short (< 100 chars)")
        if 'AAAA' in fingerprint[:50]:
            print("⚠ Warning: Fingerprint starts with 'AAAA' - might be silence")
    
    except Exception as e:
        print(f"❌ Fingerprint error: {e}")
        return
    
    # Step 3: Test AcoustID with DEMO key
    print("\n3️⃣  TESTING WITH ACOUSTID DEMO KEY...")
    
    # First, test with demo key
    demo_key = "1vOwZtEn"
    
    params = {
        'client': demo_key,
        'duration': str(int(duration)),
        'fingerprint': fingerprint,
        'meta': 'recordings',
        'format': 'json'
    }
    
    try:
        response = requests.get("https://api.acoustid.org/v2/lookup", 
                              params=params, 
                              timeout=15)
        
        print(f"HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"API Status: {data.get('status')}")
            print(f"Results: {len(data.get('results', []))}")
            
            if data.get('results'):
                print("\n🎵 DEMO KEY RESULTS:")
                for i, result in enumerate(data['results'][:3]):
                    score = result.get('score', 0)
                    if 'recordings' in result and result['recordings']:
                        recording = result['recordings'][0]
                        title = recording.get('title', 'Unknown')
                        artists = [a.get('name', 'Unknown') for a in recording.get('artists', [])]
                        print(f"  {i+1}. {score:.3f} - {title} by {', '.join(artists)}")
            else:
                print("❌ No results with DEMO key")
                print("   This means the audio is probably not in AcoustID database")
                print("   OR it's not music (ads/silence/talk)")
        
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text[:200]}")
    
    except Exception as e:
        print(f"❌ AcoustID test error: {e}")
    
    # Step 4: Test with YOUR key (if provided)
    print("\n4️⃣  TESTING WITH YOUR API KEY...")
    
    # Replace with your key
    your_key = "UK0lOjJjB7"
    
    if your_key and your_key != "YOUR_API_KEY_HERE":
        params['client'] = your_key
        
        try:
            response = requests.get("https://api.acoustid.org/v2/lookup", 
                                  params=params, 
                                  timeout=15)
            
            print(f"HTTP Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"API Status: {data.get('status')}")
                
                if data.get('status') == 'error':
                    error_msg = data.get('error', {}).get('message', 'Unknown')
                    print(f"❌ API Error: {error_msg}")
                    
                    if 'invalid' in error_msg.lower():
                        print("   Your API key appears to be INVALID")
                        print("   Get new key: https://acoustid.org/")
                
                print(f"Results: {len(data.get('results', []))}")
                
                if data.get('results'):
                    print("\n🎵 YOUR KEY RESULTS:")
                    for i, result in enumerate(data['results'][:3]):
                        score = result.get('score', 0)
                        if 'recordings' in result and result['recordings']:
                            recording = result['recordings'][0]
                            title = recording.get('title', 'Unknown')
                            artists = [a.get('name', 'Unknown') for a in recording.get('artists', [])]
                            print(f"  {i+1}. {score:.3f} - {title} by {', '.join(artists)}")
            
            else:
                print(f"❌ HTTP Error: {response.status_code}")
        
        except Exception as e:
            print(f"❌ Your key test error: {e}")
    else:
        print("⚠ Skipping (no valid API key provided)")
    
    # Step 5: Try alternative stream for comparison
    print(f"\n{'='*60}")
    print("5️⃣  COMPARING WITH KNOWN WORKING STREAM...")
    
    # Test with SomaFM (known to work)
    test_stream = "https://28513.live.streamtheworld.com/RADIO_1_ROCKAAC_H.aac"
    print(f"\nTesting with known working stream: {test_stream[:50]}...")
    
    try:
        # Quick test
        test_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        test_path = test_file.name
        test_file.close()
        
        cmd = ['ffmpeg', '-i', test_stream, '-t', '10',
               '-ar', '11025', '-ac', '1', '-y', test_path]
        subprocess.run(cmd, capture_output=True, timeout=15)
        
        if os.path.exists(test_path):
            cmd = ['fpcalc', '-json', test_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                test_data = json.loads(result.stdout)
                test_fp = test_data.get('fingerprint', '')
                test_dur = test_data.get('duration', 0)
                
                print(f"✅ Test stream fingerprint: {len(test_fp)} chars")
                
                # Compare fingerprints
                if fingerprint and test_fp:
                    similarity = sum(1 for a, b in zip(fingerprint[:100], test_fp[:100]) if a == b)
                    print(f"   Character similarity (first 100): {similarity}%")
            
            os.unlink(test_path)
    
    except Exception as e:
        print(f"⚠ Test stream error: {e}")
    
    # Cleanup
    if os.path.exists(audio_path):
        os.unlink(audio_path)
    
    print(f"\n{'='*60}")
    print("DEBUG SUMMARY:")
    print(f"{'='*60}")
    print("If NO RESULTS with demo key:")
    print("  • Stream might be playing ads/silence/talk")
    print("  • Songs might not be in AcoustID database")
    print("  • Try different stream (SomaFM works well)")
    print("\nIf YOUR KEY gives errors:")
    print("  • Your API key might be invalid")
    print("  • Get new key: https://acoustid.org/")
    print(f"{'='*60}")

def quick_test_multiple_streams():
    """Test multiple streams quickly"""
    
    print(f"{'='*60}")
    print("QUICK STREAM TESTER")
    print(f"{'='*60}")
    
    streams = [
        ("SomaFM Groove Salad", "http://ice1.somafm.com/groovesalad-128-mp3"),
        ("SomaFM Drone Zone", "http://ice2.somafm.com/dronezone-128-mp3"),
        ("Radio Paradise Rock", "http://stream.radioparadise.com/rock-128"),
        ("Your Rock Stream", "https://28513.live.streamtheworld.com/RADIO_1_ROCKAAC_H.aac"),
        ("Classic Rock", "http://stream.laut.fm/classic-rock"),
    ]
    
    for name, url in streams:
        print(f"\n🔊 Testing: {name}")
        print(f"   URL: {url[:60]}...")
        
        try:
            # Quick 5-second capture test
            temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            audio_path = temp_file.name
            temp_file.close()
            
            cmd = ['ffmpeg', '-i', url, '-t', '5', 
                   '-ar', '11025', '-ac', '1', '-y', audio_path]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and os.path.exists(audio_path):
                size_kb = os.path.getsize(audio_path) / 1024
                
                if size_kb > 10:
                    # Get fingerprint
                    cmd = ['fpcalc', '-json', audio_path]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                    
                    if result.returncode == 0:
                        data = json.loads(result.stdout)
                        fp = data.get('fingerprint', '')
                        
                        if fp and len(fp) > 50:
                            print(f"   ✅ Works (FP: {len(fp)} chars)")
                        else:
                            print(f"   ⚠ Captured but short fingerprint")
                    else:
                        print(f"   ⚠ Captured but no fingerprint")
                else:
                    print(f"   ❌ No audio captured")
            else:
                print(f"   ❌ Cannot access stream")
            
            # Cleanup
            if os.path.exists(audio_path):
                os.unlink(audio_path)
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    print("Choose debugging option:")
    print("1. Debug specific stream")
    print("2. Quick test multiple streams")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        # Your stream
        stream_url = "https://28513.live.streamtheworld.com/RADIO_1_ROCKAAC_H.aac"
        
        # Or let user input
        custom = input(f"Use default stream? (y/n): ").lower()
        if custom == 'n':
            stream_url = input("Enter stream URL: ").strip()
        
        duration = input("Capture duration (seconds, default 20): ").strip()
        duration = int(duration) if duration.isdigit() else 20
        
        debug_stream(stream_url, duration)
    
    elif choice == "2":
        quick_test_multiple_streams()
    
    else:
        print("Invalid choice")