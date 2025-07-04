import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-error-alert',
  templateUrl: './error-alert.component.html',
  styleUrls: ['./error-alert.component.scss']
})
export class ErrorAlertComponent {
  @Input() isVisible = false;
  @Input() message = '';

  hide(): void {
    this.isVisible = false;
  }
}