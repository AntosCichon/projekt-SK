def fifo(pages, frames):
    activepages = [] # pages currently loaded in memory
    faults = 0       # count of page faults
    for page in pages:
        if page not in activepages:
            # page is not in memory
            if len(activepages) == frames:
                # all memory frames are full
                activepages.pop(0) # remove oldest page from memory

            activepages.append(page) # load page to memory
            faults += 1
        continue
    
    return faults