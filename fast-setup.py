import cv2
import time
import gdal
import os
import concurrent.futures

### Replace your required output Pixel Size (m/px)
output_mppx = 0.5 

### Replace with your input TIFF images folder
input_folder = 'tiffs'


input_folder_files = os.listdir(input_folder)

st = time.time()

def process_item(input_folder_file):

    input_img = input_folder+'/'+input_folder_file

    # Extracting Image Pixel Size from Input Image
    dst = gdal.Open(input_img)
    dstt = dst.GetGeoTransform()
    dsmppx = dstt[1] * 100000
    input_mppx = round(dsmppx,2)

    # print('Input mppx =', input_mppx)
    # print('Output mppx =', output_mppx)

    # output_img = input_img[:-4]+'__'+str(input_mppx).replace('.','p')+'_to_'+str(output_mppx).replace('.','p')+input_img[-4:]
    
    output_img = input_img[:-7]+'_'+str(output_mppx).replace('.','p')+input_img[-4:]

    print(input_mppx,'to',output_mppx,'::',input_folder_file,'=>',output_img.split('/')[2])

    img =  cv2.imread(input_img)
    
    scaling_factor = input_mppx/output_mppx

    new_w = int(img.shape[1] * scaling_factor)
    new_h = int(img.shape[0] * scaling_factor)
    new_size = (new_w, new_h)

    ### cv2 ###
    resized_img = cv2.resize(img, new_size)
    cv2.imwrite(output_img, resized_img)

    # @Shahzaib (AI Dev)

    # Extract Geolocation data
    ds = gdal.Open(input_img)
    geo_transform = ds.GetGeoTransform()
    projection = ds.GetProjection()

    # Old Pixel Size (meter per pixel)
    x_mpp = geo_transform[1]
    y_mpp = geo_transform[5]

    # Updating New Pixel Size (meter per pixel)
    new_x_mpp = x_mpp * (1/scaling_factor)
    new_y_mpp = y_mpp * (1/scaling_factor)
    geo_transform = list(geo_transform)
    geo_transform[1] = new_x_mpp
    geo_transform[5] = new_y_mpp

    # Set geolocation back to a resized tif image
    ds = gdal.Open(output_img, gdal.GA_Update)
    ds.SetGeoTransform(tuple(geo_transform))
    ds.SetProjection(projection)
    ds = None

    ## @ Shahzaib (AI Dev)

    exec_time = round((time.time()-st),2)
    print('Execution time(sec):',exec_time,'-->',input_folder_file)
    # print('CPU Execution time(sec):', et_cpu-st_cpu)
    return exec_time


def main():

    st = time.time()

    items = input_folder_files

    num_workers = 18

    # Using ThreadPoolExecutor for parallel execution using threads
    # Using ProcessPoolExecutor for parallel execution using processes
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(process_item, items))

    # print("Results:", results)
    ser_time = 0.0
    for i in results:
        ser_time += float(i)
    
    par_time = round((time.time()-st),2)
    print('Total Serial time(sec):',round(ser_time,2),'(Was)')
    print('Total Parallel time(sec):',par_time,'(Now)')
    print('Speedup:',round(ser_time/par_time,2),'X')

if __name__ == "__main__":
    main()

