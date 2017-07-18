import cv2
import numpy as np
import pyradi.ryptw as ryptw
import pyradi.ryplot as ryplot

#ptwHeader = ryptw.readPTWHeader('/home/siad/PycharmProjects/SIAD/PrototypeIR/videos/MTVFlare16317806_2_frames_1_a_20.ptw')
ptwHeader = ryptw.readPTWHeader('/home/siad/PycharmProjects/SIAD/PrototypeIR/videos/MyRecord2017-07-17T210344354.seq')

ryptw.showHeader(ptwHeader)

rows = ptwHeader.h_Rows
cols = ptwHeader.h_Cols

#ryptw.showHeader(ptwHeader)

ryptw.getPTWFrame(ptwHeader, 1)

out = np.zeros(ptwHeader.data.shape, np.double)
normalized = cv2.normalize(ptwHeader.data, out, 1.0, 0.0, cv2.NORM_MINMAX)

cv2.imshow('teste', normalized)

cv2.waitKey(0)