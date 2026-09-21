from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Announcement
from courses.models import Subject

@login_required
def create_announcement(request):
    """Create a new announcement (instructors and admins)"""
    if not (request.user.is_instructor or request.user.is_admin):
        messages.error(request, 'Only instructors and administrators can create announcements.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        announcement_type = request.POST.get('announcement_type', 'system')
        subject_id = request.POST.get('subject')
        is_active = request.POST.get('is_active') == 'on'
        
        # Validation
        if not title or not content:
            messages.error(request, 'Title and content are required.')
            return redirect('announcements:create_announcement')
        
        # Create announcement
        announcement = Announcement(
            title=title,
            content=content,
            announcement_type=announcement_type,
            created_by=request.user,
            is_active=is_active
        )
        
        # If course-specific, link to subject
        if announcement_type == 'course' and subject_id:
            try:
                subject = Subject.objects.get(id=subject_id)
                # Instructors can only announce for their own subjects
                if request.user.is_instructor and subject.instructor != request.user:
                    messages.error(request, 'You can only create announcements for your own subjects.')
                    return redirect('announcements:create_announcement')
                announcement.subject = subject
            except Subject.DoesNotExist:
                messages.error(request, 'Invalid subject selected.')
                return redirect('announcements:create_announcement')
        
        announcement.save()
        messages.success(request, 'Announcement created successfully!')
        return redirect('accounts:dashboard')
    
    # Get subjects for the dropdown
    if request.user.is_instructor:
        subjects = Subject.objects.filter(instructor=request.user)
    else:  # Admin
        subjects = Subject.objects.all()
    
    context = {
        'subjects': subjects,
    }
    return render(request, 'announcements/create_announcement.html', context)


@login_required
def my_announcements(request):
    """View all announcements created by the current user"""
    if not (request.user.is_instructor or request.user.is_admin):
        messages.error(request, 'Access denied.')
        return redirect('accounts:dashboard')
    
    announcements = Announcement.objects.filter(
        created_by=request.user
    ).select_related('subject').order_by('-created_at')
    
    context = {
        'announcements': announcements,
    }
    return render(request, 'announcements/my_announcements.html', context)


@login_required
def edit_announcement(request, announcement_id):
    """Edit an existing announcement"""
    announcement = get_object_or_404(Announcement, id=announcement_id)
    
    # Check permission
    if announcement.created_by != request.user and not request.user.is_admin:
        messages.error(request, 'You can only edit your own announcements.')
        return redirect('announcements:my_announcements')
    
    if request.method == 'POST':
        announcement.title = request.POST.get('title', '').strip()
        announcement.content = request.POST.get('content', '').strip()
        announcement.announcement_type = request.POST.get('announcement_type', 'system')
        announcement.is_active = request.POST.get('is_active') == 'on'
        
        # Update subject if course-specific
        if announcement.announcement_type == 'course':
            subject_id = request.POST.get('subject')
            if subject_id:
                try:
                    subject = Subject.objects.get(id=subject_id)
                    if request.user.is_instructor and subject.instructor != request.user:
                        messages.error(request, 'You can only link to your own subjects.')
                        return redirect('announcements:edit_announcement', announcement_id=announcement_id)
                    announcement.subject = subject
                except Subject.DoesNotExist:
                    messages.error(request, 'Invalid subject selected.')
                    return redirect('announcements:edit_announcement', announcement_id=announcement_id)
        else:
            announcement.subject = None
        
        announcement.save()
        messages.success(request, 'Announcement updated successfully!')
        return redirect('announcements:my_announcements')
    
    # Get subjects for the dropdown
    if request.user.is_instructor:
        subjects = Subject.objects.filter(instructor=request.user)
    else:
        subjects = Subject.objects.all()
    
    context = {
        'announcement': announcement,
        'subjects': subjects,
    }
    return render(request, 'announcements/edit_announcement.html', context)


@login_required
def delete_announcement(request, announcement_id):
    """Delete an announcement"""
    announcement = get_object_or_404(Announcement, id=announcement_id)
    
    # Check permission
    if announcement.created_by != request.user and not request.user.is_admin:
        messages.error(request, 'You can only delete your own announcements.')
        return redirect('announcements:my_announcements')
    
    if request.method == 'POST':
        announcement.delete()
        messages.success(request, 'Announcement deleted successfully!')
        return redirect('announcements:my_announcements')
    
    return redirect('announcements:my_announcements')

