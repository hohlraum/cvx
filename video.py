# -*- coding: utf-8 -*-
"""
A quick attempt at Pythonizing the interface to OpenCV
"""

import cv2

def fourcc_int2str(n):    
    """
    Convert fourcc integer into a four letter code
    
    """
    n=int(n)
    out= chr(n & 0XFF)\
        +chr(n>>8 & 0XFF)\
        +chr(n>>16 & 0XFF)\
        +chr(n>>24 & 0XFF)

    return out

class VideoCapture(object):
    """
    A video source available for capture
    """
    def __init__(self, src):
        """
        Open the source        
        """
        self._src=cv2.VideoCapture(src)
        self.src=src        

    def read(self):
        """
        Read the next frame        
        """
        flag, img=self._src.read()

        if flag is False:
            raise EOFError('Reached the end of video')
        return img

    def release(self):
        """
        Close the source        
        """
        self._src.release()
        
    def set_frame(self, frame_num):
        """
        Set the next frame for acquisition
        """
        self._src.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frame_num)

    def get_frames(self):
        """
        Get the number of the next frame for acquisition
        """
        return int(self._src.get(cv2.cv.CV_CAP_PROP_POS_FRAMES))

    def set_height(self, height):
        """
        Set the height of the frame
        """
        self._src.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)

    def get_height(self):
        """
        Get the height of the frame
        """
        return int(self._src.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

    def set_width(self, width):
        """
        Set the width of the frame
        """
        self._src.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)

    def get_width(self):
        """
        Get the width of the frame
        """
        return int(self._src.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))

    def set_fps(self, fps):
        """
        Set the framerate
        """
        self._src.set(cv2.cv.CV_CAP_PROP_FPS, fps)
    
    def get_fps(self):
        """
        Get the framerate
        """
        return self._src.get(cv2.cv.CV_CAP_PROP_FPS)

    def set_fourcc(self, fourcc):
        """
        Set the encoding
        
        fourcc is a four character string (e.g. 'MJPG')
        """
        fourcc=cv2.cv.CV_FOURCC(*tuple(fourcc))
        self._src.set(cv2.cv.CV_CAP_PROP_FOURCC, fourcc)

    def get_fourcc(self):
        """
        Set the encoding        
        """
        fourcc=self._src.get(cv2.cv.CV_CAP_PROP_FOURCC)

        return fourcc_int2str(fourcc)
        
    def __enter__(self):
        """
        Enter context manager
        """
        return self
        
    def __exit__(self, type, value, tb):
        """
        Exit context manager        
        """
        self._src.release()
        
    def __iter__(self):
        """
        Iterate over the fames of the source
        """
        self.set_frame(0)
        return self
        
    def next(self):
        """
        Return the next frame
        """
        try:
            return self.read()
        except EOFError:
            raise StopIteration                
        
    def __len__(self):
        """
        Return the number of frames
        """
        return int(self._src.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

    def __getitem__(self, frames):
        """
        Get frame(s)
        
        Slices return a list of images
        """
        if type(frames) is slice:
            return [self[i] for i in range(*frames.indices(len(self)))]
        
        else:
            self.set_frame(frames)
            return self.read()
    


class VideoWriter(object):
    """
    A video destination for writing
    """
    def __init__(self, fname, fourcc='MJPG', fps=5, frame_size=(640,480), is_color=True):
        """
        Open the source 
        
        frame_size is (widht,height)
        """
        self.fname=fname
        self.fourcc=fourcc        
        self.fps=fps
        self.frame_size=frame_size
        self.is_color= is_color
        
        fourcc=cv2.cv.CV_FOURCC(*tuple(fourcc))
        
        self._writer=cv2.VideoWriter(fname, fourcc, fps, frame_size, 1*is_color)

    def release(self):
        """
        Close the writer        
        """
        self._writer.release()
        
    def __enter__(self):
        """
        Enter context manager
        """
        return self
        
    def __exit__(self, type, value, tb):
        """
        Exit context manager        
        """
        self.release()
        
    def write(self, img):
        """
        Write a frame
        """
        self._writer.write(img)
    
    def isOpened(self):
        """
        Return open state
        """
        return 1==self._writer.isOpened()