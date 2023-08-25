import cv2
import time
import gdal
import sys

# read image
# st_cpu = time.process_time()

def main():

    # The first argument (index 0) is the script name itself
    script_name = sys.argv[0]
    
    # Check if at least one command-line argument is provided
    if len(sys.argv) < 2:
        print("Usage: python {} [inputImg] [pixelSize]".format(script_name))
        sys.exit(1)

    # Access command-line arguments starting from index 1
    arguments = sys.argv[1:]

    input_img = arguments[0]
    output_mppx = float(arguments[1])

    st = time.time()
    

    # Extracting Image Pixel Size from Input Image
    dst = gdal.Open(input_img)
    dstt = dst.GetGeoTransform()
    dsmppx = dstt[1] * 100000
    input_mppx = round(dsmppx,2)

    print('Input mppx =', input_mppx)
    print('Output mppx =', output_mppx)

    output_img = input_img[:-4]+'__'+str(input_mppx).replace('.','p')+'_to_'+str(output_mppx).replace('.','p')+input_img[-4:]

    # print('Before Read Execution time(sec):',round((time.time()-st),2))
    img =  cv2.imread(input_img)

    # print('After Read Execution time(sec):',round((time.time()-st),2))

    scaling_factor = input_mppx/output_mppx

    new_w = int(img.shape[1] * scaling_factor)
    new_h = int(img.shape[0] * scaling_factor)
    new_size = (new_w, new_h)

    resized_img = cv2.resize(img, new_size)


    # print('After Resize Execution time(sec):',round((time.time()-st),2))
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


    print('Execution time(sec):',round((time.time()-st),2))
    # print('CPU Execution time(sec):', et_cpu-st_cpu)

if __name__ == "__main__":
    main()