import pygame
import random
import math
pygame.init()

# -----------------------------------------------GENERATING A WINDOW TO REPRESENT THE SORTING ALGORITHMS-------------------------------------------------  
class DrawInformation:
    BLACK=0,0,0
    WHITE=255,255,255
    GREEN=0,255,0
    RED=255,0,0
    BACKGROUND_COLOUR=WHITE
    GRADIENTS=[
         (128,128,128),
         (160,160,160),
         (192,192,192)
    ]
    FONT=pygame.font.SysFont('comicsans',30)
    LARGE_FONT=pygame.font.SysFont('comicsans',40)
    SIDE_PAD=100
    TOP_PAD=150
    
    def __init__(self,width,height,lst):
        self.width=width
        self.height=height
        self.window = pygame.display.set_mode((width,height)) # generating an attribute to access the  window,generating an attribute to access the window pass height and width as tuple
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst) 
        
    def set_list(self,lst):
            self.lst=lst
            self.min_val=min(lst)
            self.max_val=max(lst)
            # width of each block
            self.block_width=round((self.width-self.SIDE_PAD)/len(lst))
            self.block_height=math.floor((self.height-self.TOP_PAD)/(self.max_val-self.min_val))
            # to give side padding on the x-axis
            self.start_x=self.SIDE_PAD//2
            
def draw(draw_info,algo_name,ascending):
     draw_info.window.fill(draw_info.BACKGROUND_COLOUR) #to give background colour of your liking
    
     title=draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}",1,draw_info.BLACK)
     draw_info.window.blit(title,(draw_info.width/2-title.get_width()/2,5))
 
     controls=draw_info.FONT.render("R-Reset | SPACE - Start Sorting | A-Ascending | D- Descending",1,draw_info.BLACK)
     draw_info.window.blit(controls,(draw_info.width/2-controls.get_width()/2,50))

     sorting=draw_info.FONT.render("I-Insertion Sort | B - Bubble Sort | S-Selection Sort | M-Merge Sort | Q-Quick Sort | H-Heap Sort",1,draw_info.BLACK)
     draw_info.window.blit(sorting,(draw_info.width/2-sorting.get_width()/2,85))

     draw_list(draw_info)
     pygame.display.update()

def draw_list(draw_info,colour_position={},clear_bg=False):
     lst=draw_info.lst
     if clear_bg:
          clear_rect=(draw_info.SIDE_PAD//2,draw_info.TOP_PAD,draw_info.width-draw_info.SIDE_PAD,
                      draw_info.height-draw_info.TOP_PAD)
          pygame.draw.rect(draw_info.window,draw_info.BACKGROUND_COLOUR,clear_rect)
     for i,val in enumerate(lst):
          x=draw_info.start_x+i*draw_info.block_width # block_width is single unit of width given e.g 1cm=1unit
        #   height of screen - (value at that index-min_val)*single unit of height given e.g 1cm=1unit
          y=draw_info.height-(val-draw_info.min_val)*draw_info.block_height # going to draw the rectangle from top to bottom
          colour=draw_info.GRADIENTS[i%3] # to repeat 3 colours periodically
          if i in colour_position:
              colour=colour_position[i] 
          #inputs to draw function- window on which it has to draw , colour,x coordinate,y coordinate , width till which it should draw,height till which it should draw
          pygame.draw.rect(draw_info.window,colour,(x,y,draw_info.block_width,draw_info.height))

     if clear_bg:
	     pygame.display.update()     

		# --------------------------------------------GENERATING A STARTING LIST------------------------------------------------------

def generate_starting_list(n,min_value,max_value):
    lst=[]
    for _ in range(n):
        val=random.randint(min_value,max_value)
        lst.append(val)
    return lst

def bubble_sort(draw_info,ascending=True):
    lst=draw_info.lst
    for i in range(len(lst)-1):
          for j in range(len(lst)-1-i):
               num1=lst[j]
               num2=lst[j+1]

               if(num1>num2 and ascending) or (num1<num2 and not ascending):
                    lst[j],lst[j+1]=lst[j+1],lst[j]
                    draw_list(draw_info,{j:draw_info.GREEN,j+1:draw_info.RED},True)
                    yield True #return back to the start point
    return lst 

def insertion_sort(draw_info,ascending=True):
     lst=draw_info.lst
     for i in range(1,len(lst)):
          current=lst[i]
          while True:
               ascending_sort=i>0 and lst[i-1]>current and ascending
               descending_sort=i>0 and lst[i-1]<current and not ascending

               if not ascending_sort and not descending_sort:
                    break
               lst[i]=lst[i-1]
               i=i-1
               lst[i]=current
               draw_list(draw_info,{i-1:draw_info.GREEN,i:draw_info.RED},True)
               yield True

     return lst

def selection_sort(draw_info,ascending=True):
     lst=draw_info.lst
     size=len(lst)
     for ind in range(size):
          min_index = ind
          for j in range(ind + 1, size):
            # select the minimum element in every iteration
            if lst[j] < lst[min_index]:
                min_index = j
         # swapping the elements to sort the array
          (lst[ind], lst[min_index]) = (lst[min_index],lst[ind])
          draw_list(draw_info,{ind-1:draw_info.GREEN,ind:draw_info.RED},True)
          yield True

     return lst

def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2
 
 # See if left child of root exists and is greater than root
    if l < n and arr[i] < arr[l]:
        largest = l
 
 # See if right child of root exists and is greater than root
    if r < n and arr[largest] < arr[r]:
        largest = r

 # Change root, if needed
    if largest != i:
        (arr[i], arr[largest]) = (arr[largest], arr[i])  # swap
 
  # Heapify the root.
        heapify(arr, n, largest)
 
def heap_sort(draw_info,ascending=True):
     lst=draw_info.lst
     n = len(lst)
 
 # Build a maxheap.
 # Since last parent will be at ((n//2)-1) we can start at that location.
     for i in range(n // 2 - 1, -1, -1):
        heapify(lst, n, i)
 
 # One by one extract elements
     for i in range(n - 1, 0, -1):
        (lst[i], lst[0]) = (lst[0], lst[i])  # swap
        heapify(lst, i, 0)
        draw_list(draw_info,{i-1:draw_info.GREEN,i:draw_info.RED},True)
        yield True

     return lst

def merge_sort(draw_info,ascending=True):
    ret = []
    lst=draw_info.lst
    if( len(lst) == 1):
        return lst
    half  = len(lst) / 2
    lower = merge_sort(lst[:half],ascending)
    upper = merge_sort(lst[half:],ascending) 
    lower_len = len(lower)
    upper_len = len(upper)
    i = 0
    j = 0
    while i != lower_len or j != upper_len:
        if(i != lower_len and (j == upper_len or lower[i] < upper[j])):
            ret.append(lower[i])
            i += 1
        else:
            ret.append(upper[j])
            j += 1

        draw_list(draw_info,{i-1:draw_info.GREEN,j:draw_info.RED},True)
        yield True

    return ret

def main():
    run=True
    # to regulate how quickly the loop  run
    clock=pygame.time.Clock()
    n=50
    min_val=0
    max_val=100
    lst=generate_starting_list(n,min_val,max_val)
    draw_info=DrawInformation(1500,700,lst)
    sorting=False
    ascending=True

    sorting_algorithm=bubble_sort
    sorting_algo_name="Bubble Sort"
    sorting_algorithm_generator=None
    # to prevent the event from ending immediately we run a loop in pygame
    while run:
        clock.tick(10) #the loop can run max 60 times per second

        if sorting:
               try:
                  next(sorting_algorithm_generator)
               except StopIteration:
                    sorting=False
        else:
          draw(draw_info,sorting_algo_name,ascending)
     #    pygame.display.update()

        for event in pygame.event.get():
                if event.type==pygame.QUIT: #to quit the visualizer
                     run=False
                #to press the R key to reset the type of sorting algorithm implementing
                if event.type!=pygame.KEYDOWN:
                     continue
                if event.key==pygame.K_r: # K_r reprents R key on the keyboard
                     lst=generate_starting_list(n,min_val,max_val)
                     draw_info.set_list(lst)
                     sorting=False

                elif event.key==pygame.K_SPACE and sorting==False: # K_SPACE reprents Space key on the keyboard
                     sorting=True
                     sorting_algorithm_generator=sorting_algorithm(draw_info,ascending) 

                elif event.key==pygame.K_a and not sorting: # K_a reprents A key on the keyboard
                     ascending=True

                elif event.key==pygame.K_d and not sorting: # K_d reprents D key on the keyboard
                     ascending=False

                elif event.key==pygame.K_i and not sorting: # K_i reprents I key on the keyboard
                     sorting_algorithm=insertion_sort
                     sorting_algo_name="Insertion Sort"

                elif event.key==pygame.K_b and not sorting: # K_b reprents B key on the keyboard
                     sorting_algorithm=bubble_sort
                     sorting_algo_name="Bubble Sort"

                elif event.key==pygame.K_s and not sorting: # K_s reprents S key on the keyboard
                     sorting_algorithm=selection_sort
                     sorting_algo_name="Selection Sort"

                elif event.key==pygame.K_h and not sorting: # K_h reprents H key on the keyboard
                     sorting_algorithm=heap_sort
                     sorting_algo_name="Heap Sort"

                elif event.key==pygame.K_m and not sorting: # K_m reprents M key on the keyboard
                     sorting_algorithm=merge_sort
                     sorting_algo_name="Merge Sort"


    pygame.quit()   

if __name__ == "__main__":
	main()               



            
                 
                          