#!/usr/bin/env python3

import cv2
import os
import argparse
import time


def remove_line(write_file_name, img_file):
    write_file = open(write_file_name, 'r') 
    file_lines = write_file.readlines()
    write_file.close()
    write_file = open(write_file_name, 'w+')
    for line in file_lines:
        if line.rstrip() != img_file.rstrip():
            write_file.write(line)
    write_file.close()


def main():
    time_inital = time.time()
    
    parser = argparse.ArgumentParser("Analyze detected 3G-AMP images")
    parser.add_argument("--optical_analysis_file", help="Text file to load optical detections from", default = "data/full_optical_analysis.txt")
    parser.add_argument("--true_results_file", help="Text file to load true detections from", default = "data/strem_YOLO_optical_dections_true.txt")
    
    parser.add_argument("--start", help="Quantity to start analysis at", default = 0, type=int)
    
    parser.add_argument("--true_write_name", help="Text file to write true detections to", default = "verifications/verified_true_detections.txt")
    parser.add_argument("--false_write_name", help="Text file to write false detections to", default = "verifications/verified_false_detections.txt")
    
    parser.add_argument("--last_image_save_file", help="Text file to write true last_image_visited", default = "data/last_visted_img.txt")
    parser.add_argument("--resume", help="Resume classification from last known start location", default = False, type=bool)
                                  
                                  
    args = parser.parse_args() 
    #yoloVideoStream = YoloLiveVideoStream(args)
    
    true_write_name=args.true_write_name
    false_write_name=args.false_write_name
    
    true_file =  open(args.true_results_file, 'r')
    true_data_lines = [line.rstrip().split(',')[-1] for line in true_file.readlines()]   
    
    all_data_file = open(args.optical_analysis_file, 'r')
    all_data_lines = [line.rstrip() for line in all_data_file.readlines()]
    
    
    if args.resume:
        save_img_file = open(args.last_image_save_file, 'r')
        save_lines = save_img_file.readlines()
        img_num = int(save_lines[-1].rstrip())
        save_img_file.close()
    else:
        img_num=args.start
    
    print("Press 'Enter' to classify event as true. Press 'p' to pause stream. Press 'b' to go back 1 image if paused. press 'n' to go forward 1 image if paused. Press 'c' to continue stream if paused")
    print("If event is incorrectly classified as true, move back to the image and press 'f' to remove it from the false.")
    print("Press 'q' to quit")
    print("To resume from last location, set --resume True on start. Alternativly, set --start <num> to start from a specific location")
    
    waitTime = 0
    while img_num < len(all_data_lines):
        print(img_num)
        if (all_data_lines[img_num].split(',')[-1]  not in true_data_lines):
            img_file = all_data_lines[img_num]
            #print(img_file.split(',')[-1].rstrip())
            img = cv2.imread(img_file.split(',')[-1].rstrip())
            #detection, mean_iou = yoloVideoStream.stream_img(img)
            
            cv2.imshow('img', img)
            k = cv2.waitKey(waitTime)
            print("Time elapsed:", time.time() - time_inital)
            print("Current file num:", img_num)
            print(k)
            if k == 117: #u
                print("UNUSRE")
                unsure_write_file = open(true_write_name.replace('true', 'unsure'), 'a+')
                unsure_write_file.write(img_file.split(',')[-1])
                unsure_write_file.close()
            
            elif k == 13 or k == 116: # 'enter' or 't'
                print('TRUE CLASSIFICATION')
                ''' TRUE '''
                if os.path.exists(false_write_name):
                    remove_line(false_write_name, img_file.split(',')[-1]) 
                    
                true_write_file = open(true_write_name, 'a+')
                true_write_file.write(img_file.split(',')[-1]+'\n')
                true_write_file.close()
                
                
            elif k == 102: # f
                print('FALSE CLASSIFICATION')
                ''' False '''
                if os.path.exists(true_write_name):
                    remove_line(true_write_name, img_file.split(',')[-1])    
                    
                false_write_file = open(false_write_name, 'a+')
                false_write_file.write(img_file.split(',')[-1] +'\n')
                false_write_file.close()
                
            elif k == 98: #b
                print('GOING BACKWARDS')
                '''
                GO BACK
                '''
                img_num -= 1
                continue
                
            elif k == 113: #q
                print('EXITING')
                ''' Exit '''
                exit()
            elif k != -1:
                print("No valid key selected. 'Enter' for true, 'f' for false, 'b' for back 1 image, 'n' for next image, and 'q' for quit")
                continue
            
        
        img_num += 1
        save_img_file = open(args.last_image_save_file, 'a+')
        save_img_file.write(str(img_num) +'\n')
        save_img_file.close()
        
            
        
        
    
if __name__ == '__main__':
    main()    
        