#!/usr/bin/env python
"""
Script to extract all video URLs from the database and save them to a text file.
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from api.models import Video, CourseVideo, UpcomingEvent, PrayerRoom, Devotion, VideoTranslation, Stream

def extract_video_urls():
    """Extract all video URLs from the database."""
    urls = []
    
    # Get URLs from Video model
    try:
        videos = Video.objects.all()
        for video in videos:
            if video.youtube_url:
                urls.append(f"Video: {video.title} - {video.youtube_url}")
        print(f"Found {videos.count()} videos")
    except Exception as e:
        print(f"Error accessing Video model: {e}")
    
    # Get URLs from CourseVideo model
    try:
        course_videos = CourseVideo.objects.all()
        for cv in course_videos:
            if cv.youtube_url:
                urls.append(f"Course Video: {cv.name} - {cv.youtube_url}")
        print(f"Found {course_videos.count()} course videos")
    except Exception as e:
        print(f"Error accessing CourseVideo model: {e}")
    
    # Get URLs from UpcomingEvent model (past events)
    try:
        events = UpcomingEvent.objects.filter(event_status='past')
        for event in events:
            if event.youtube_url:
                urls.append(f"Event: {event.title} - {event.youtube_url}")
        print(f"Found {events.count()} past events")
    except Exception as e:
        print(f"Error accessing UpcomingEvent model: {e}")
    
    # Get URLs from PrayerRoom model
    try:
        prayer_rooms = PrayerRoom.objects.all()
        for pr in prayer_rooms:
            if pr.youtube_url:
                urls.append(f"Prayer Room: {pr.title} - {pr.youtube_url}")
        print(f"Found {prayer_rooms.count()} prayer rooms")
    except Exception as e:
        print(f"Error accessing PrayerRoom model: {e}")
    
    # Get URLs from Devotion model (video type only)
    try:
        devotions = Devotion.objects.filter(content_type='video')
        for devotion in devotions:
            if devotion.youtube_url:
                urls.append(f"Devotion: {devotion.title} - {devotion.youtube_url}")
        print(f"Found {devotions.count()} video devotions")
    except Exception as e:
        print(f"Error accessing Devotion model: {e}")
    
    # Get URLs from VideoTranslation model
    try:
        translations = VideoTranslation.objects.all()
        for vt in translations:
            if vt.translated_video_url:
                urls.append(f"Translation ({vt.language_display}): {vt.translated_video_url}")
        print(f"Found {translations.count()} translations")
    except Exception as e:
        print(f"Error accessing VideoTranslation model: {e}")
    
    # Get URLs from Stream model
    try:
        streams = Stream.objects.all()
        for stream in streams:
            if stream.stream_url:
                urls.append(f"Stream: {stream.title} - {stream.stream_url}")
        print(f"Found {streams.count()} streams")
    except Exception as e:
        print(f"Error accessing Stream model: {e}")
    
    return urls

def save_urls_to_file(urls, filename='video_urls.txt'):
    """Save URLs to a text file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Video URLs extracted from database\n")
        f.write("=" * 50 + "\n\n")
        
        if urls:
            for i, url in enumerate(urls, 1):
                f.write(f"{i}. {url}\n")
            f.write(f"\nTotal URLs: {len(urls)}\n")
        else:
            f.write("No video URLs found in the database.\n")
    
    print(f"Successfully saved {len(urls)} video URLs to {filename}")

if __name__ == '__main__':
    try:
        print("Extracting video URLs from database...")
        urls = extract_video_urls()
        save_urls_to_file(urls)
        print("Done!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
