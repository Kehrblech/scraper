import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../api-service/api-service.component';

interface SlideContent {
  type: string;
  value: string;
  imageUrl?: string; // optional property for image URLs
}

interface Slide {
  mainTitle: string;
  title: string;
  text: SlideContent[];
}

@Component({
  selector: 'app-slideshow',
  templateUrl: './slideshow.component.html',
  styleUrls: ['./slideshow.component.css']
})
export class SlideShowComponent implements OnInit {
  slides: Slide[] = [];
  isLoading: boolean = false;
  currentSlideIndex: number = 0;
  url: string = '';
  isFullscreen = false;


  constructor(private route: ActivatedRoute, private apiService: ApiService) { }

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      const url = params['url'];
      if (url) {
        this.fetchData(url);
      }
    });
  }

  toggleFullscreen() {
    this.isFullscreen = !this.isFullscreen;
  }



  // fetchData(url: string) {
  //   this.isLoading = true;
  //   this.apiService.getData(url).subscribe((data: any) => {
  //     console.log(data); // Überprüfen Sie die empfangenen Daten

  //     this.slides = [];

  //     for (const key in data) {
  //       if (data.hasOwnProperty(key)) {
  //         const section = data[key];
  //         const mainTitle = key;
  //         for (const subsectionKey in section) {
  //           if (section.hasOwnProperty(subsectionKey)) {
  //             if (subsectionKey === 'Inhaltsverzeichnis') {
  //               continue;
  //             }

  //             if (subsectionKey === 'Weblinks' || subsectionKey === 'Einzelnachweise') {
  //               continue;
  //             }

  //             const subsection = section[subsectionKey];
  //             const title = subsectionKey;
  //             const text: SlideContent[] = [];

  //             const subsubsectionKeys = Object.keys(subsection);
  //             if (subsubsectionKeys.length > 0) {
  //               const subsubsectionTitle = subsubsectionKeys[0];
  //               const subsubsectionTextArray = Array.isArray(subsection[subsubsectionTitle]) ? subsection[subsubsectionTitle] : [subsection[subsubsectionTitle]];
  //               const subsubsectionText = subsubsectionTextArray.map((value: string) => {
  //                 if (typeof value === 'string' && (value.startsWith('//') || value.startsWith('http://') || value.startsWith('https://'))) {
  //                   return { type: 'image', value, imageUrl: value };
  //                 } else {
  //                   return { type: 'text', value };
  //                 }
  //               });

  //               text.push({ type: 'subtitle', value: subsubsectionTitle });
  //               text.push(...subsubsectionText);
  //             }

  //             for (const contentKey in subsection) {
  //               if (subsection.hasOwnProperty(contentKey)) {
  //                 if (contentKey === subsubsectionKeys[0]) {
  //                   continue;
  //                 }

  //                 const contentArray = Array.isArray(subsection[contentKey]) ? subsection[contentKey] : [subsection[contentKey]];
  //                 const content = contentArray.map((value: string) => {
  //                   if (typeof value === 'string' && (value.startsWith('//') || value.startsWith('http://') || value.startsWith('https://'))) {
  //                     return { type: 'image', value, imageUrl: value };
  //                   } else {
  //                     return { type: 'text', value };
  //                   }
  //                 });

  //                 text.push({ type: 'subtitle', value: contentKey });
  //                 text.push(...content);
  //               }
  //             }

  //             this.slides.push({ mainTitle, title, text });
  //           }
  //         }
  //       }
  //     }

  //     this.isLoading = false;
  //   });
  // }

  fetchData(url: string) {
    this.isLoading = true;
    this.apiService.getData(url).subscribe((data: any) => {
      console.log(data); // Verify the received data

      this.slides = this.convertJsonToSlides(data);
      this.isLoading = false;
    });
  }

  convertJsonToSlides(data: any): Slide[] {
    const slides: Slide[] = [];

    for (const slideData of data.slides) {
      const slide: Slide = {
        mainTitle: slideData.name,
        title: '',
        text: []
      };

      if (slideData.images && slideData.images.length > 0 && slideData.text && slideData.text.length > 0){
        for (const image of slideData.images) {
          const imageUrl = image.url;
          slide.text.push({ type: 'image', value: imageUrl, imageUrl });
        }
        const textValue = Array.isArray(slideData.text) ? slideData.text.join(' ') : slideData.text;
        slide.text.push({ type: 'text', value: textValue });
        slides.push(slide);
      }

    }

    return slides;
  }

  nextSlide() {
    this.currentSlideIndex = (this.currentSlideIndex + 1) % this.slides.length;
  }
  lastSlide() {
    this.currentSlideIndex = (this.currentSlideIndex - 1) % this.slides.length;
  }
}


