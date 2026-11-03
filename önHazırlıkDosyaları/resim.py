import os
from PIL import Image

def crop_image(input_path, output_path):
    """Tek bir görseli 135px kenarlardan kırparak 293x293 yapar."""
    try:
        with Image.open(input_path) as img:
            # Koordinat sırası: (sol, üst, sağ, alt)
            # sağ = 563 - 135 = 428
            # alt = 563 - 135 = 428
            #left = 135
            #upper = 135
            #right = 428
            #lower = 428
            
            # sağ = 563 - 100 = 463
            # alt = 563 - 100 = 463
            left = 135
            upper = 180
            right = 428
            lower = 473
            

            cropped_img = img.crop((left, upper, right, lower))
            
            # Hedef dosyanın klasör yolu yoksa oluştur
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            cropped_img.save(output_path, "PNG")
            #print(f"Başarıyla kırpıldı: {output_path}")
    except Exception as e:
        print(f"Hata oluştu ({input_path}): {e}")

def batch_crop_recursive(input_dir, output_dir):
    """Girdi klasöründeki tüm iç içe klasörleri ve .png dosyalarını tarayarak kırpar."""
    if not os.path.exists(input_dir):
        print(f"Hata: Girdi klasörü bulunamadı: {input_dir}")
        return

    # os.walk ile alt klasörler dahil tüm dosyaları tarıyoruz
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            
            
            if filename.find("patla")!=-1:
                continue

            if filename.lower().endswith('.png'):
                # Girdi klasörüne göre dosyanın göreceli (relative) yolunu bul
                input_path = os.path.join(root, filename)
                rel_path = os.path.relpath(input_path, input_dir)
                
                # Çıktı klasöründeki tam yolu oluştur
                output_path = os.path.join(output_dir, rel_path)
                
                crop_image(input_path, output_path)

if __name__ == "__main__":
    girdi_klasoru = "orijinaller"
    cikis_klasoru = "kirpilmis"
    
    batch_crop_recursive(girdi_klasoru, cikis_klasoru)