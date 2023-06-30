import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SlideShowComponent } from './slideshow.component';

describe('SlideshowComponent', () => {
  let component: SlideShowComponent;
  let fixture: ComponentFixture<SlideShowComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SlideShowComponent]
    });
    fixture = TestBed.createComponent(SlideShowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
