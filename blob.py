import cv
import itertools

class ConnectedComponent:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.count = 0

    def __str__(self):
        return "%d %d %d %d count %d"%(self.x1, self.x2, self.y1, self.y2, self.count)
        
class BlobDetector:
    ''' Union-find functions taken from http://code.activestate.com/recipes/577225-union-find/ '''
    class _Node:
        def __init__ (self, label):
            self.label = label
        def __str__(self):
            return self.label
        
    def _MakeSet(self, x):
         x.parent = x
         x.rank   = 0

    def _Union(self, x, y):
        xRoot = self._Find(x)
        yRoot = self._Find(y)
        if xRoot.rank > yRoot.rank:
            yRoot.parent = xRoot
        elif xRoot.rank < yRoot.rank:
            xRoot.parent = yRoot
        elif xRoot != yRoot: # Unless x and y are already in same set, merge them
            yRoot.parent = xRoot
            xRoot.rank = xRoot.rank + 1

    def _Find(self, x):
        if x.parent == x:
            return x
        else:
            x.parent = self._Find(x.parent)
            return x.parent
            
    def _AddBorder(self, image):
        # Write 1px black border
        for j in xrange(image.width):
            image[0, j] = 0
            image[image.height-1, j] = 0
            
        for i in xrange(image.height):
            image[i, 0] = 0
            image[i, image.width-1] = 0          
        
    def _Relabel(self, img_label, uf):
        roi = {}
        
        for i in xrange(1, img_label.height):
            for j in xrange(1, img_label.width):
                if img_label[i, j] == 0:
                    continue
                    
                label = self._Find(uf[int(img_label[i, j]-1)]).label
                img_label[i, j] = label
                
                cc = roi.setdefault(label, ConnectedComponent(j, j, i, i))
                cc.x1 = min(cc.x1, j)
                cc.x2 = max(cc.x2, j)
                cc.y1 = min(cc.y1, i)
                cc.y2 = max(cc.y2, i)
                cc.count += 1  

        return roi                
       
    def detect(self, image):
        img_label = cv.CloneMat(image)
        
        self._AddBorder(img_label)
        
        uf = []
        
        label = 1;
        
        for i in xrange(1, image.height):
            for j in xrange(1, image.width):
                current = (i, j)
                if image[current] == 0:
                    continue
                    
                north = (i-1, j)
                south = (i+1, j)
                east = (i, j+1)
                west = (i, j-1)
                    
                # Do the pixels to the North and West of the current pixel have the same value but not the same label?                
                if (image[north] == image[west] and image[west] != 0) and (img_label[north] != img_label[west]):
                    # Merge
                    min_label = min(img_label[north], img_label[west])
                    max_label = max(img_label[north], img_label[west])
                                        
                    img_label[current] = min_label
                    
                    self._Union(uf[int(min_label)-1], uf[int(max_label)-1])                   
                # Does the pixel to the left (West) have the same value?
                elif image[west] == image[current]:
                    img_label[current] = img_label[west]   
                # Does the pixel to the left (West) have a different value and the one to the North the same value?
                elif (image[west] !=0 and image[west] != image[current]) and (image[north] == image[current]):
                    img_label[current] = img_label[north]
                else:
                    img_label[current] = label
                    node = self._Node(label)
                    self._MakeSet(node)
                    uf.append(node)
                    label = label + 1
                    
        # Relabel every labeled pixel with its representative           
        return self._Relabel(img_label, uf)
        
                                       
if __name__=="__main__": 
    detector = BlobDetector()
    img = cv.LoadImageM('test.png', cv.CV_LOAD_IMAGE_GRAYSCALE)
    for i in xrange(img.height):
        for j in xrange(img.width):
            if img[i, j] != 0:
                img[i, j] = 1               
                                   
    detector.detect(img)
