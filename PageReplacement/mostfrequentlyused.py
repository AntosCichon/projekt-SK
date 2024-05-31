def mfu(pages, frames):
    activepages = [] # pages currently loaded
    faults = 0  # page faults counter
    pagesfrequency = {} # frequency of page usage

    for page in pages:
        if page not in activepages:

            if len(activepages) == frames:
                # if memory frames are full, find most frequently used page and remove it from pagesfrequency and activepages
                mostused = max(activepages, key=pagesfrequency.get)
                del pagesfrequency[activepages.pop(activepages.index(mostused))]

            activepages.append(page) # load requested page
            faults += 1 # increment faults counter
            pagesfrequency[page] = 1 # set this page frequency of usage to 1
            
        else:
            # if requested page is already loaded, increment its usage frequency
            pagesfrequency[page] = pagesfrequency.get(page, 0) + 1
    

    return faults