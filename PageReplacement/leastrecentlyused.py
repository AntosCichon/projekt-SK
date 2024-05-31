def lru(pages, frames):
    activepages = [] # pages currently loaded, where firts is the oldest and last is most recently used
    faults = 0 # count of page faults

    for page in pages:

        if page not in activepages:

            if len(activepages) == frames: # if memory frames are full, find the oldest page and remove it from memory
                activepages.pop(0)

            activepages.append(page) # load new page to memory
            faults += 1 # increment faults counter

        else:
            activepages.append(activepages.pop(activepages.index(page))) # if this page is already loaded, move it to the end of activepages (making it the youngest)

    return faults