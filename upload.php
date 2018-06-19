<?php 
//https://github.com/ethicalhack3r/DVWA/blob/master/vulnerabilities/upload/source/impossible.php
header("Access-Control-Allow-Origin:*");
if( empty($_FILES['pic']['tmp_name']) || !($_FILES['pic']['size'] > 0 )){
    header("Access-Control-Allow-Headers:content-type");
    header("Access-Control-Request-Method:POST");
    echo "upload\n";
}
else{
    // File information
    $uploaded_name = $_FILES[ 'pic' ][ 'name' ];
    $uploaded_ext  = substr( $uploaded_name, strrpos( $uploaded_name, '.' ) + 1);
    $uploaded_size = $_FILES[ 'pic' ][ 'size' ];
    $uploaded_type = $_FILES[ 'pic' ][ 'type' ];
    $uploaded_tmp  = $_FILES[ 'pic' ][ 'tmp_name' ];
    $img_info = getimagesize( $uploaded_tmp );
    // Where are we going to be writing to?
    $target_path   = './f/';
    $target_file   =  date("YmdHis").rand(1000, 9999) . '.png';
    $temp_file     = ( ( ini_get( 'upload_tmp_dir' ) == '' ) ? ( sys_get_temp_dir() ) : ( ini_get( 'upload_tmp_dir' ) ) );
    $temp_file    .= DIRECTORY_SEPARATOR . md5( uniqid() . $uploaded_name ) . '.' . $uploaded_ext;
    // Is it an image?
    $msg = '';
    $url = '';
    if( $uploaded_size > 1000000 ) $msg = 'pic too big, upload failed';
    else if( ( strtolower( $uploaded_ext ) == 'png' ) &&
        ( $uploaded_type === 'image/png' ) &&
        $img_info ) {
        $img = imagecreatefrompng( $uploaded_tmp );
        $font = "./AlphaSmart3000.ttf";
        $black = imagecolorallocate($img, 0, 0, 0);
        imagefttext($img, 13, 0, intval($img_info[0])-60, intval($img_info[1])-20, $black, $font, 'zzz');
        imagepng( $img, $temp_file );
        imagedestroy( $img );
        // Can we move the file to the web root from the temp folder?
        if( rename( $temp_file, ( $target_path . $target_file ) ) ) {
            // Yes!
            $msg = 'upload succeeded';
            $url = "http://zzz/f/".$target_file;
        }
        else {
            // No
            $msg = 'Your image was not uploaded.';
        }
        // Delete any temp files
        if( file_exists( $temp_file ) )
            unlink( $temp_file );
    }
    else {
        // Invalid file
        $msg = 'Your image was not uploaded. We can only accept PNG images.';
    }
    echo json_encode(array('msg'=>$msg, 'url'=>$url));
}
