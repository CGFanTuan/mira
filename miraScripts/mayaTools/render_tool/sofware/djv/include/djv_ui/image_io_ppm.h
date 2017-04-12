/*------------------------------------------------------------------------------
 lib/djv_ui/image_io_ppm.h
 
 Copyright (c) 2004-2009 Darby Johnston
 All rights reserved.
 Use is subject to license terms.
------------------------------------------------------------------------------*/

#ifndef DJV_UI_IMAGE_IO_PPM_H
#define DJV_UI_IMAGE_IO_PPM_H

#include <djv_image/io_ppm.h>
#include <djv_ui/image_io.h>

namespace djv_ui {

//------------------------------------------------------------------------------
//!\namespace djv_ui::image_io_ppm
//
//! PPM plugin - Image I/O widgets.
//------------------------------------------------------------------------------

namespace image_io_ppm {

//------------------------------------------------------------------------------
//!\class Save
//
//! Save user-interface plugin.
//------------------------------------------------------------------------------

class _DJV_UI Save : public image_io::Save
{
public:

  //----------------------------------------------------------------------------
  //!\name Construction
  //@{

  Save();
  
  ~Save();

  //@}
  //----------------------------------------------------------------------------
  //!\name Plugin
  //@{

  plugin::Plugin * copy() const;
  
  String name() const;

  //@}
  //----------------------------------------------------------------------------
  //!\name Value
  //@{
  
  void set(djv_image::io::Base *);

  //@}
  
private:

  DJV_CALLBACK(Save, type_callback, int);
  DJV_CALLBACK(Save, data_callback, int);
  
  void plugin_update();
  void widget_update();

  djv_image::io::Base * _plugin;
  djv_image::io_ppm::Save_Option _option;

  struct _Save;
  std::auto_ptr<_Save> _p;
};

//------------------------------------------------------------------------------
//!\name Labels
//------------------------------------------------------------------------------
//@{

_DJV_UI extern const String
  label_type_group,
  label_data_group;

//@}
//------------------------------------------------------------------------------

}
}

#endif

