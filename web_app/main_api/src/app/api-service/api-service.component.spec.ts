import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApiService } from './api-service.component';

describe('ApiServiceComponent', () => {
  let component: ApiService;
  let fixture: ComponentFixture<ApiService>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ApiService]
    });
    fixture = TestBed.createComponent(ApiService);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
