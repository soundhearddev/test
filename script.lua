; Datei: tas_frame_step.ahk
; Alt+F1 führt eine Eingabe + 1 Frame aus

!F1::
    Send, {b down}
    Sleep, 30  ; Halte Taste 30ms
    Send, {b up}

    SetSpeed(0.2)
    Sleep, 50
    SetSpeed(0.0)
return

SetSpeed(speed)
{
    Run, "C:\Path\To\Cheat Engine\SpeedhackInject.exe" %speed%
}
