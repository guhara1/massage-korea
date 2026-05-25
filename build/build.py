# -*- coding: utf-8 -*-
"""사이트 생성기 진입점. `python build/build.py` 실행 → dist/ 생성."""

import os
import shutil
import pages
from data import SERVICES, REGIONS, THERAPISTS


def main():
    if os.path.isdir(pages.OUT):
        shutil.rmtree(pages.OUT)
    os.makedirs(pages.OUT, exist_ok=True)

    pages.build_home()
    pages.build_service_index()
    for s in SERVICES:
        pages.build_service_detail(s)
    pages.build_pricing()
    pages.build_reviews()
    pages.build_about()
    pages.build_contact()
    pages.build_locations_index()
    for key, v in REGIONS.items():
        pages.build_metro_hub(key, v)
        for slug, dname in v["districts"]:
            pages.build_district(key, v, slug, dname)
    pages.build_therapists_index()
    for t in THERAPISTS:
        pages.build_therapist_detail(t)
    pages.build_policies()
    pages.build_meta_files()

    print(f"생성 완료: {len(pages.SITEMAP)} 페이지 → {pages.OUT}")
    for p, pr, cf in sorted(set(pages.SITEMAP)):
        print(f"  {pr}  {p}")


if __name__ == "__main__":
    main()
