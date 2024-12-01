import streetview
from concurrent.futures import ThreadPoolExecutor
from typing import List


class GooglePanaromaMultithreadDownloaderer:

    debug: bool
    save_path: str

    def __int__(self, debug: bool = True, save_path: str = 'ai_results/'):
        self.debug = debug
        self.save_path = save_path

    def __worker(self, current_coords: str):
        if self.debug:
            print("Current coords:", current_coords)
        lat, lon = current_coords.split(", ")
        panos = streetview.search_panoramas(lat=lat, lon=lon)
        panos_l = len(panos)
        for i, pan in enumerate(panos, 1):
            if self.debug:
                print(current_coords, "->", pan.pano_id, f"{i}/{panos_l}")
            image = streetview.get_panorama(pano_id=pan.pano_id)
            image.save(f"{self.save_path}{current_coords}__{pan.pano_id}__000.jpg", "jpeg")


    def download(self, coords: List[str], max_threads: int = 4):
        if not coords:
            return
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            for c in coords:
                executor.submit(lambda: self.__worker(c))
            executor.shutdown()

pd = GooglePanaromaMultithreadDownloaderer()
pd.download(["35.441125, 139.644649", "35.634721, 140.360978", "35.701562, 139.776285", "35.361453, 139.625891"])
