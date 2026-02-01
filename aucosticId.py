#!/usr/bin/env python3
"""
FINAL WORKING Radio Stream Song Recognizer
"""

import asyncio
import aiohttp
import subprocess
import tempfile
import json
import os
import time
from datetime import datetime
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RadioSongDetector:
    def __init__(self, acoustid_api_key):
        """
        Initialize detector with AcoustID API key
        
        Args:
            acoustid_api_key: Get FREE key from https://acoustid.org/
        """
        if not acoustid_api_key or acoustid_api_key == "YOUR_API_KEY_HERE":
            print("\n❌ ERROR: Invalid API key!")
            print("Get FREE key: https://acoustid.org/")
            sys.exit(1)
        
        self.api_key = acoustid_api_key
        self.fpcalc_path = self._find_fpcalc()
        
        if not self.fpcalc_path:
            print("❌ fpcalc not found. Install: sudo apt install libchromaprint-tools")
            sys.exit(1)
        
        print(f"✅ System ready. Using API key: {self.api_key[:8]}...")
    
    def _find_fpcalc(self):
        """Find fpcalc executable"""
        try:
            result = subprocess.run(['which', 'fpcalc'], 
                                   capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        for path in ['/usr/bin/fpcalc', '/usr/local/bin/fpcalc']:
            if os.path.exists(path):
                return path
        
        return None
    
    def capture_stream_chunk(self, stream_url, duration=20):
        """
        Capture audio chunk from stream with better error handling
        
        Returns:
            Path to temp audio file or None
        """
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_path = temp_file.name
        temp_file.close()
        
        try:
            # Try multiple ffmpeg approaches
            commands = [
                # Method 1: Direct capture
                ['ffmpeg', '-i', stream_url, '-t', str(duration),
                 '-ar', '11025', '-ac', '1', '-acodec', 'pcm_s16le',
                 '-y', '-loglevel', 'quiet', temp_path],
                
                # Method 2: With buffer settings
                ['ffmpeg', '-i', stream_url, '-t', str(duration),
                 '-ar', '11025', '-ac', '1', '-f', 'wav',
                 '-y', '-loglevel', 'quiet', temp_path],
            ]
            
            for cmd in commands:
                try:
                    # Run with timeout
                    process = subprocess.Popen(cmd, 
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
                    
                    stdout, stderr = process.communicate(timeout=duration + 15)
                    
                    if process.returncode == 0:
                        if os.path.exists(temp_path) and os.path.getsize(temp_path) > 50000:
                            size_mb = os.path.getsize(temp_path) / (1024 * 1024)
                            logger.debug(f"Captured {size_mb:.2f} MB")
                            return temp_path
                    
                except subprocess.TimeoutExpired:
                    process.kill()
                    continue
                except Exception:
                    continue
            
            return None
            
        except Exception as e:
            logger.error(f"Capture error: {e}")
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            return None
    
    def get_fingerprint(self, audio_file):
        """
        Generate fingerprint from audio file
        
        Returns:
            tuple: (duration, fingerprint) or (None, None)
        """
        try:
            # Try different fpcalc options
            options = [
                [self.fpcalc_path, '-json', '-length', '120', audio_file],
                [self.fpcalc_path, '-json', audio_file],
            ]
            
            for cmd in options:
                try:
                    result = subprocess.run(cmd, 
                                          capture_output=True, 
                                          text=True, 
                                          timeout=15)
                    
                    if result.returncode == 0:
                        data = json.loads(result.stdout)
                        duration = data.get('duration', 0)
                        fingerprint = data.get('fingerprint', '')
                        
                        if fingerprint and len(fingerprint) > 50 and duration > 5:
                            return duration, fingerprint
                            
                except Exception:
                    continue
            
            return None, None
            
        except Exception as e:
            logger.error(f"Fingerprint error: {e}")
            return None, None
    
    async def identify_song(self, duration, fingerprint):
        """
        Identify song using AcoustID with detailed response
        
        Returns:
            dict: Song info or None
        """
        url = "https://api.acoustid.org/v2/lookup"
        
        params = {
            'client': self.api_key,
            'duration': str(int(duration)),
            'fingerprint': fingerprint,
            'meta': 'recordings releases tracks',
            'format': 'json'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=20) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # DEBUG: Print full response
                        print(f"\n{'='*60}")
                        print("ACOUSTID RESPONSE:")
                        print(f"Status: {data.get('status')}")
                        print(f"Results: {len(data.get('results', []))}")
                        
                        if data.get('status') == 'ok' and data.get('results'):
                            results = data['results']
                            
                            # Show all results for debugging
                            for i, result in enumerate(results):
                                score = result.get('score', 0)
                                print(f"\nResult {i+1}: Score = {score:.4f}")
                                
                                if 'recordings' in result and result['recordings']:
                                    recording = result['recordings'][0]
                                    title = recording.get('title', 'Unknown')
                                    artists = [a.get('name', 'Unknown') 
                                              for a in recording.get('artists', [])]
                                    print(f"  Title: {title}")
                                    print(f"  Artist: {', '.join(artists)}")
                                    
                                    if 'releases' in recording and recording['releases']:
                                        print(f"  Album: {recording['releases'][0].get('title')}")
                            
                            # Get best match
                            best_result = max(results, key=lambda x: x.get('score', 0))
                            score = best_result.get('score', 0)
                            
                            if score > 0.15 and 'recordings' in best_result:  # Low threshold
                                recording = best_result['recordings'][0]
                                
                                return {
                                    'title': recording.get('title', 'Unknown'),
                                    'artists': [a.get('name', 'Unknown') 
                                               for a in recording.get('artists', [])],
                                    'score': score,
                                    'duration': duration,
                                    'timestamp': datetime.now().isoformat(),
                                    'all_results': len(results)
                                }
                        
                        print(f"No confident matches (best score < 0.15)")
                        return None
                    
                    else:
                        print(f"HTTP Error: {response.status}")
                        return None
                        
        except Exception as e:
            print(f"AcoustID error: {e}")
            return None
    
    async def test_stream(self, stream_url, duration=15):
        """
        Test if stream can be processed
        """
        print(f"\n{'='*60}")
        print(f"TESTING STREAM: {stream_url[:80]}...")
        print(f"{'='*60}")
        
        # 1. Capture
        print("1. Capturing audio...")
        audio_path = self.capture_stream_chunk(stream_url, duration)
        
        if not audio_path:
            print("   ❌ Capture failed")
            return False
        
        file_size = os.path.getsize(audio_path)
        print(f"   ✅ Captured {file_size/1024:.1f} KB")
        
        # 2. Fingerprint
        print("2. Generating fingerprint...")
        fp_duration, fingerprint = self.get_fingerprint(audio_path)
        
        # Clean up
        if os.path.exists(audio_path):
            os.unlink(audio_path)
        
        if not fingerprint:
            print("   ❌ No fingerprint")
            return False
        
        print(f"   ✅ Fingerprint: {fp_duration:.1f}s, {len(fingerprint)} chars")
        print(f"   FP sample: {fingerprint[:50]}...")
        
        # 3. Identify
        print("3. Identifying song...")
        song_info = await self.identify_song(fp_duration, fingerprint)
        
        if song_info:
            print(f"\n   ✅ SONG DETECTED!")
            print(f"      Title: {song_info['title']}")
            print(f"      Artist: {', '.join(song_info['artists'])}")
            print(f"      Confidence: {song_info['score']:.1%}")
            return True
        else:
            print("   ⚠ No song identified")
            print("\n   Possible reasons:")
            print("   - Ads/silence/talk was playing")
            print("   - Song not in AcoustID database")
            print("   - Try longer capture (30+ seconds)")
            return True  # Stream is working even if no match
    
    async def monitor_stream(self, stream_url, interval=45, chunk_duration=20):
        """
        Continuous monitoring with better detection
        """
        print(f"\n{'='*60}")
        print("LIVE MONITORING STARTED")
        print(f"{'='*60}")
        print(f"Stream: {stream_url}")
        print(f"Check every: {interval}s")
        print(f"Analyze: {chunk_duration}s chunks")
        print(f"{'='*60}")
        print("Press Ctrl+C to stop\n")
        
        detection_count = 0
        last_song = None
        
        while True:
            try:
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"\n[{current_time}] Cycle #{detection_count + 1}")
                
                # Capture
                print(f"[{current_time}] Capturing {chunk_duration}s...")
                audio_path = self.capture_stream_chunk(stream_url, chunk_duration)
                
                if not audio_path:
                    print(f"[{current_time}] ❌ Capture failed")
                    await asyncio.sleep(10)
                    continue
                
                # Fingerprint
                duration, fingerprint = self.get_fingerprint(audio_path)
                
                # Clean up
                if os.path.exists(audio_path):
                    os.unlink(audio_path)
                
                if not fingerprint:
                    print(f"[{current_time}] ❌ No fingerprint")
                    await asyncio.sleep(interval - chunk_duration)
                    continue
                
                # Identify
                print(f"[{current_time}] Identifying...")
                song_info = await self.identify_song(duration, fingerprint)
                
                if song_info:
                    current_song = f"{song_info['title']} - {', '.join(song_info['artists'])}"
                    
                    # Avoid duplicate detection
                    if last_song != current_song and song_info['score'] > 0.2:
                        detection_count += 1
                        last_song = current_song
                        
                        print(f"\n{'🎵'*30}")
                        print(f"🎵 DETECTION #{detection_count} [{current_time}]")
                        print(f"{'🎵'*30}")
                        print(f"Title: {song_info['title']}")
                        print(f"Artist(s): {', '.join(song_info['artists'])}")
                        print(f"Confidence: {song_info['score']:.1%}")
                        print(f"Duration: {duration:.1f}s")
                        print(f"Results found: {song_info.get('all_results', 0)}")
                        print(f"{'🎵'*30}\n")
                        
                        # Save to file
                        with open('radio_detections.log', 'a') as f:
                            f.write(f"{current_time} | {song_info['title']} | "
                                   f"{', '.join(song_info['artists'])} | "
                                   f"{song_info['score']:.3f} | {duration:.1f}s\n")
                    else:
                        print(f"[{current_time}] Same song or low confidence")
                else:
                    print(f"[{current_time}] No match")
                
                # Wait for next check
                wait_time = max(10, interval - chunk_duration)
                print(f"[{current_time}] Next check in {wait_time}s...")
                await asyncio.sleep(wait_time)
                
            except KeyboardInterrupt:
                print(f"\n\n{'='*60}")
                print(f"MONITORING STOPPED")
                print(f"Total detections: {detection_count}")
                print(f"{'='*60}")
                break
            except Exception as e:
                print(f"\n[{current_time}] Error: {e}")
                await asyncio.sleep(10)

async def main():
    """Main function"""
    print(f"{'='*60}")
    print("RADIO STREAM SONG DETECTOR")
    print(f"{'='*60}")
    
    # ============================================
    # IMPORTANT: Replace with YOUR AcoustID API key
    # Get FREE key: https://acoustid.org/
    # ============================================
    API_KEY = "MygGaT3XJt"  # Your key (keep this if it works)
    
    # If using demo key for testing (limited)
    # API_KEY = "1vOwZtEn"  # AcoustID demo key
    
    # List of streams to try (most reliable first)
    STREAMS = [
      
        # Your original stream
        "https://28513.live.streamtheworld.com/RADIO_1_ROCKAAC_H.aac",
    ]
    
    # Create detector
    detector = RadioSongDetector(acoustid_api_key=API_KEY)
    
    # Test each stream
    working_streams = []
    
    for i, stream_url in enumerate(STREAMS):
        print(f"\n\nTesting stream {i+1}/{len(STREAMS)}...")
        
        try:
            # Test with 20-second capture
            success = await detector.test_stream(stream_url, duration=20)
            
            if success:
                print(f"\n✅ Stream {i+1} WORKS!")
                working_streams.append(stream_url)
                
                # Ask if user wants to monitor this stream
                response = input(f"\nStart monitoring this stream? (y/n): ").lower()
                if response == 'y':
                    await detector.monitor_stream(
                        stream_url=stream_url,
                        interval=45,      # Check every 45 seconds
                        chunk_duration=20  # Analyze 20-second chunks
                    )
                    return  # Exit after monitoring
            else:
                print(f"\n❌ Stream {i+1} failed")
                
        except Exception as e:
            print(f"\n⚠ Stream {i+1} error: {e}")
        
        await asyncio.sleep(2)
    
    # If we get here, no stream was selected for monitoring
    if working_streams:
        print(f"\n\n{'='*60}")
        print("WORKING STREAMS FOUND:")
        for i, stream in enumerate(working_streams):
            print(f"{i+1}. {stream}")
        
        print(f"\nTo monitor a stream, modify the code to select one.")
    else:
        print(f"\n\n❌ No working streams found.")
        print("Try:")
        print("1. Check internet connection")
        print("2. Try different streams")
        print("3. Test streams in VLC first")

if __name__ == "__main__":
    # System check
    print("System check...")
    
    # Check dependencies
    dependencies = [
        ('ffmpeg', 'ffmpeg -version', 'sudo apt install ffmpeg'),
        ('fpcalc', 'which fpcalc', 'sudo apt install libchromaprint-tools'),
    ]
    
    all_ok = True
    for name, cmd, install_cmd in dependencies:
        try:
            if 'which' in cmd:
                result = subprocess.run(cmd.split(), 
                                      capture_output=True, 
                                      timeout=2)
                ok = result.returncode == 0
            else:
                result = subprocess.run(cmd.split()[:2], 
                                      capture_output=True, 
                                      timeout=2)
                ok = result.returncode == 0
            
            if ok:
                print(f"✅ {name}")
            else:
                print(f"❌ {name} missing")
                print(f"   Install: {install_cmd}")
                all_ok = False
                
        except Exception:
            print(f"❌ {name} check failed")
            all_ok = False
    
    if not all_ok:
        sys.exit(1)
    
    # Check Python packages
    try:
        import aiohttp
        print("✅ aiohttp")
    except ImportError:
        print("❌ aiohttp missing")
        print("   Install: pip install aiohttp")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    
    # Run main
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()