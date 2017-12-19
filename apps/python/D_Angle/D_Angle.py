import ac
import acsys
import math

#configure
MaxAngle = 130
MinKMH = 10

#label
AngleLabel = 0
PeakAngleLabel = 0
PeakKMHLabel = 0

#field
Angle = 0
PeakAngle = 0
Timer = 0

def acMain(ac_version):
    global AngleLabel, PeakAngleLabel, PeakKMHLabel

    # init Window
    appWindow = ac.newApp("D_Angle")
    ac.setSize(appWindow, 200, 113)
    ac.setTitle(appWindow, "D_Angle")
    ac.drawBorder(appWindow, 0)
    ac.setBackgroundOpacity(appWindow, 0.1)

    # label configure
    AngleLabel = ac.addLabel(appWindow, "0°")
    ac.setPosition(AngleLabel, 100, 20)
    ac.setFontAlignment(AngleLabel, "center")
    ac.setFontSize(AngleLabel, 55)
    ac.setFontColor(AngleLabel, 1, 1, 1, 1)

    PeakAngleLabel = ac.addLabel(appWindow, "0°")
    ac.setPosition(PeakAngleLabel, 110, 87)
    ac.setFontAlignment(PeakAngleLabel, "right")
    ac.setFontSize(PeakAngleLabel, 12)
    ac.setFontColor(PeakAngleLabel, 1, 1, 1, 0.6)

    PeakKMHLabel = ac.addLabel(appWindow, "0")
    ac.setPosition(PeakKMHLabel, 130, 87)
    ac.setFontAlignment(PeakKMHLabel, "right")
    ac.setFontSize(PeakKMHLabel, 12)
    ac.setFontColor(PeakKMHLabel, 1, 1, 1, 0.6)

    peakTitleLabel = ac.addLabel(appWindow, "peak :")
    ac.setPosition(peakTitleLabel, 50, 87)
    ac.setFontAlignment(peakTitleLabel, "left")
    ac.setFontSize(peakTitleLabel, 10)
    ac.setFontColor(peakTitleLabel, 1, 1, 1, 0.6)

    peakKMHUnitLabel = ac.addLabel(appWindow, "km/h")
    ac.setPosition(peakKMHUnitLabel, 135, 90)
    ac.setFontAlignment(peakKMHUnitLabel, "left")
    ac.setFontSize(peakKMHUnitLabel, 8)
    ac.setFontColor(peakKMHUnitLabel, 1, 1, 1, 0.6)


def acUpdate(deltaT):
    global AngleLabel, Angle, PeakAngleLabel, PeakAngle, Timer, MinKMH, PeakKMHLabel
    ac.setFontAlignment(AngleLabel, "center")
    ac.setPosition(AngleLabel, 100, 20)

    # raw data
    carKMH = ac.getCarState(0, acsys.CS.SpeedKMH)
    fl, fr, rl, rr = ac.getCarState(0, acsys.CS.SlipAngle)
    vx, vy, vz = ac.getCarState(0, acsys.CS.LocalVelocity)

    # model data
    Angle = getDriftAngle(rl, rr, vz)

    # spin : over angle
    if Angle > MaxAngle and carKMH > MinKMH:
        ac.setText(AngleLabel, "Spin")
        ac.setText(peakKMHLabel, "0")
        PeakAngle = 0
        return

    # spin : lower speed
    if Angle > 60 and carKMH < MinKMH and vz > 0:
        ac.setText(AngleLabel, "Spin")
        ac.setText(peakKMHLabel, "0")
        PeakAngle = 0
        return

    # drifting
    if carKMH > MinKMH:
        ac.setText(AngleLabel, "{:.0f}°".format(Angle))
        if Angle > PeakAngle:
            PeakAngle = Angle
            ac.setText(PeakAngleLabel, "{:.0f}°".format(PeakAngle))
            ac.setText(PeakKMHLabel, "{:.0f}".format(carKMH))
    # Wait anim
    else:
        ac.setPosition(AngleLabel, 37, 20)
        Timer += deltaT
        ac.setFontAlignment(AngleLabel, "left")
        if int(Timer) % 3 == 0:
            ac.setText(AngleLabel, "ready")
        if int(Timer) % 3 == 1:
            ac.setText(AngleLabel, "ready.")
        if int(Timer) % 3 == 2:
            ac.setText(AngleLabel, "ready..")

        PeakAngle = 0
        ac.setText(PeakAngleLabel, "{:.0f}°".format(PeakAngle))
        ac.setText(PeakKMHLabel, "0")

def getDriftAngle(rl, rr, vz):
    rawAngle = math.fabs(round(rl+rr)/2)
    if vz <= 0:
        return 180 - rawAngle
    else:
        return rawAngle


