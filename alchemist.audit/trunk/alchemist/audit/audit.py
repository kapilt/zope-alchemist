"""
Auditing of Changes for Domain Objects.

implementation note, we dance around with attaching change ids to the
events, to do a crude coalesce in band to the event subscribers, as
workflow state changes are also modification events.
"""

import interfaces

def objectAdded( ob, event):
    auditor = interfaces.IRecorder( ob )
    auditor.objectAdded( event )
    
def objectModified( ob, event ):
    auditor = interfaces.IRecorder( ob )  
    if getattr( event, 'change_id', None):
        return
    auditor.objectModified(event )    
    
def objectDeleted( ob, event ):
    auditor = interfaces.IRecorder( ob )    
    auditor.objectDeleted( event )        

def objectStateChange( ob, event ):
    auditor = interfaces.IRecorder( ob )
    change_id = auditor.objectStateChanged( event )
    event.change_id = change_id
    
def objectNewVersion( ob, event ):
    auditor = interfaces.IRecorder( ob )
    if not getattr( event, 'change_id', None):
        change_id = auditor.objectNewVersion( event )
    else:
        change_id = event.change_id
    event.version.change_id = change_id

def objectRevertedVersion( ob, event ):
    # slightly obnoxious hand off between event handlers (objectnewV, objectrevertedV),
    # stuffing onto the event for value passing
    auditor = interfaces.IRecorder( ob )
    change_id = auditor.objectRevertedVersion( event )   
    event.change_id = change_id
    

